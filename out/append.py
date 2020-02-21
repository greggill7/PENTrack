#!/usr/bin/env python
#from __future__ import print_function
import numpy as np
import pandas as pd
import argparse
import os.path
import sys
import h5py
import time


def main():
    parser = argparse.ArgumentParser(description='Appends .out files onto hdf5')
    parser.add_argument('-r', '--runs', type=int, nargs='+', required=True, help='PENTrack runs to append')
    parser.add_argument('-f', '--file', type=str, required=True, help='Name of hdf file to create/append to')
    parser.add_argument('-t', '--type', type=str, choices=['end', 'spin', 'track', 'hit'], default='end', help='File type to append (default = end)')
    parser.add_argument('-p', '--path', type=str, help = '.out files folder location (default ./)', default='./')
    parser.add_argument('-mwt', '--maxWaitTime', type=int, default=5, 'Max number of minutes spent waiting for lock file to disappear (default 5 min)')
    parser.add_argument('-clev', '--compLevel', type=int,  default=9, help = 'Compression level [0-9]. 0 disables compression. Default=9')
    parser.add_argument('-clib', '--compLib', type=str, default='bzip2', help = 'Compression library (default bzip2)' )
    args = parser.parse_args()

    lockfile = 'append.lock'

    if (args.path[-1] != '/'):
        path = args.path + '/'
    else:
        path = args.path

    # Check for lock file. Create one if all clear
    waitTime = 0 #
    while os.path.isfile(lockfile):
        time.sleep(30)
        waitTime += 0.5
        if waitTime >= args.maxWaitTime:
            print('Max buffer time exceeded. Exiting')
            return

    print('Creating ', lockfile)
    np.savetxt(lockfile, args.runs, header='Current runs being appended', fmt='%1i')

    try:
        toHdf(args.runs, path, args.file, 'neutron' + args.type + '.out', args.compLevel, args.compLib)
    finally:
        if os.path.isfile(lockfile): # Remove lockfile at all costs
            os.remove( lockfile )

    return

def toHdf( runNums, folder, outputFilename, filetype, clev, clib, hdfKey='neutrons'):
    simTotal = 0
    missedRuns = []

    # Check if hdf file already exists. If so, get attributes
    # If hdf file is missing attributes, read in the particle column
    if os.path.isfile(outputFilename):
        with h5py.File(OUTPUT_FILENAME, "r") as fout:
            if 'totalParticles' in fout.attrs:
                simTotal = fout.attrs['totalParticles']
                print('Total particles in current hdf file: ', simTotal)
            else:
                print('No totalParticles attribute found in existing hdf file')
                df = pd.read_hdf(args.file, hdfkey, columns=['particle'])
                simTotal = len(df.index)
                print(outputFilename, ' has ', simTotal, ' particles')
                del df

    else:
        print('Creating ', outputFilename)

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
        print('\nNo ' + filetype + ' files read')
    else:
        print('\nError reading run numbers-- ', missedRuns)
        print('Total particles: ', simTotal)
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
