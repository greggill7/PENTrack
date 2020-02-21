#!/usr/bin/env python
#from __future__ import print_function
import numpy as np
import pandas as pd
import argparse
import os.path
import h5py
import sys

def main():
    parser = argparse.ArgumentParser(description='Compresses neutronspin.out, track.out, hit.out, and end.out files into hdf5')
    parser.add_argument('-r', '--runs', type=int, nargs=2, required=True, help='Start and end values of PENTrack runs')
    parser.add_argument('-f', '--folder', type=str, help = '.out files folder location (default ./)', default='./')
    parser.add_argument('-clev', '--compLevel', type=int, help = 'Compression level [0-9]. 0 disables compression. Default=9', default=9)
    parser.add_argument('-clib', '--compLib', type=str, help = 'Compression library (default bzip2)', default='bzip2')
    args = parser.parse_args()

    if args.runs[1] < args.runs[0]:
        print('ERROR: Invalid [--runs] range')
        return
    else:
        runNums = np.arange(args.runs[0],args.runs[1]+1)

    if (args.folder[-1] != '/'):
        folder = args.folder + '/'
    else:
        folder = args.folder

    print('Reading end.out files...')
    toHdf( runNums, folder, 'neutronend.out', args.compLevel, args.compLib )

    print('Reading hit.out files...')
    toHdf( runNums, folder, 'neutronhit.out', args.compLevel, args.compLib )

    print('Reading spin.out files...')
    toHdf( runNums, folder, 'neutronspin.out', args.compLevel, args.compLib )

    print('Reading track.out files...')
    toHdf( runNums, folder, 'neutrontrack.out', args.compLevel, args.compLib )

    return

def toHdf( runNums, folder, filetype, clev, clib, hdfKey='neutrons'):
    simTotal = 0
    missedRuns = []

    if len(runNums) == 1:
        outputFilename = folder + str(runNums[0]) + noExt(filetype, '.out') + '.hdf'
    else:
        outputFilename = folder + str(runNums[0]) + '-' + str(runNums[-1]) + noExt(filetype, '.out') + '.hdf'

    if os.path.isfile(outputFilename):
        print("ERROR: ", outputFilename, " already exists!")
        return

    for i in runNums:
        runName = folder + str(i).zfill(12) + filetype
        try:    # Catch errors when either reading file or if file isn't there
            if not os.path.isfile(runName):
                missedRuns.append(i)
                continue
            print(i,'...', end='')
            sys.stdout.flush()
            df = pd.read_csv(runName, delim_whitespace=True).astype('float64')
        except:
            missedRuns.append(i)
            continue

        # Correctly number neutrons, update simulation total
        df['particle'] += simTotal
        df.index += simTotal
        simTotal += len(df.index)

        df.to_hdf(outputFilename, key=hdfKey, format='t', data_columns=True, mode='a', append=True, complib=clib, complevel=clev, dropna=True)

    if len(missedRuns) == len(runNums):
        print('No ' + filetype + ' files read')
    else:
        print('Error reading run numbers-- ', missedRuns)
        print('Total neutrons in file: ', simTotal)
        print('Saved to ', outputFilename, '\n')

        # Update hdf attribute
        with h5py.File(outputFilename, "r+") as f:
            f.attrs['totalParticles'] = simTotal

    return

# Removes the extension name from a filename if present
def noExt(filename, extensionName):
    if filename[-len(extensionName):].find(extensionName) != -1:
        return filename[:-len(extensionName)]
    return filename

if ( __name__ == '__main__' ):
    main()
