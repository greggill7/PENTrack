#!/usr/bin/env python
# Calcs t2 from neutronspin.out files, examines Sx and Sy component falling
# out of sync

#from __future__ import print_function
import numpy as np
import argparse
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.optimize import curve_fit
import sys
import os

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def fit(t, b, c):
    # Function for fitting <Sx>
    return np.exp(-(t - c) / b )

# Guess for parameters to fit
guess = [100, 5]

def main():
    parser = argparse.ArgumentParser(description='Calculates T2 from multiple neutronspin.out files (Chris Swank method)')
    parser.add_argument('-r', '--runs', type=int, nargs=2, required=True, help='Start and end values of PENTrack runs')
    parser.add_argument('-f', '--folder', type=str, help = 'Folder location (default ./)', default='./')
    parser.add_argument('-t', '--time', type=float, nargs=2, required=True, help='Start and end values of T2 precession time')
    parser.add_argument('-s', '--step', type=float, nargs=1, required=True, help='Step size in [range] with which to calculate T2')
    parser.add_argument('-o', '--output', type=str, help = 'Output file name of fit and <Sx>. If file name already exists, reads from file, and ignores -r -f -t -s')
    args = parser.parse_args()

    if args.output:
        exists = os.path.isfile(args.output)
    else:
        exists = False

    if exists:
        # Read <Sx> from pre-existing file
        print('Reading from ', args.output)
        t2Times, sxAv, syAv = np.genfromtxt(args.output, unpack=True)
    else:

        if (args.folder[-1] != '/'):
            folder = args.folder + '/'
        else:
            folder = args.folder

        print('Reading files and processing...')
        runNum = np.arange(args.runs[0],args.runs[1]+1)
        t2Times = np.arange(args.time[0],args.time[1] + args.step[0],args.step[0])
        simTotal = 0
        missedRuns = []
        sxT2 = np.zeros(len(t2Times))
        syT2 = np.zeros(len(t2Times))


        for i in runNum:
            runName = folder + str(i).zfill(12) + 'neutronspin.out'
            print(i,'...', end='')
            sys.stdout.flush()      # Yes, I know print has a flush=True option. Doesn't work in python2
            try:
                df = pd.read_csv(runName, delim_whitespace=True, usecols=[1, 2, 6, 7]).drop_duplicates(subset='t', keep='first')
                # Columns are titled 'particle, t, Sx, Sy'
            except:
                missedRuns.append(i)
                continue

            simTotal += df['particle'].iloc[-1]

            for particleNum in np.arange(1, df['particle'].iloc[-1] + 1 ):
                # Skip canceled runs
                if t2Times[-2] > df.query('particle == @particleNum')['t'].iloc[-1]:
                    simTotal -= 1
                    print(df.query('particle == @particleNum')['t'].iloc[-1])
                    continue
                # Interpolate
                try:
                    interpX = InterpolatedUnivariateSpline(df.query('particle == @particleNum')['t'], df.query('particle == @particleNum')['Sx'])
                    interpY = InterpolatedUnivariateSpline(df.query('particle == @particleNum')['t'], df.query('particle == @particleNum')['Sy'])
                    sxT2 = sxT2 + np.array(interpX(t2Times))
                    syT2 = syT2 + np.array(interpY(t2Times))
                except:
                    simTotal -= 1

        print('Done')
        print('Error reading run numbers-- ', missedRuns)
        print('Number of neutrons simulated: ', simTotal)

        # Find average for sx set
        sxAv = sxT2/simTotal
        syAv = syT2/simTotal

        if args.output:
            print('Saving t2Times, <Sx>, <Sy> to ', args.output)
            np.savetxt(args.output, np.c_[t2Times, sxAv, syAv])

    # Fit function for T2
    print('\nFitting function:')
    print('np.exp(-(t - c) / b )')
    print('Guessed parameters (edit in file)')
    print('[b,c]')
    print(guess)

    decayCurve = np.sqrt( np.square(sxAv) + np.square(syAv) )

    popt, pcov = curve_fit(fit, t2Times, decayCurve, p0=guess)
    print('Fitted parameters')
    print(popt)
    print('+/- [',np.sqrt(pcov[0][0]),', ', np.sqrt(pcov[1][1]), ']')


    if args.output:
        # Plotting
        print('\nPlotting...')
        fig = plt.figure()
        plt.plot(t2Times, decayCurve,color='C0')
        plt.plot(t2Times, fit(t2Times, *popt), color='C1',label='fit')
        plt.grid(True)
        plt.xlabel('t [s]')
        plt.ylabel('<Sx>^2+<Sy>^2')
        plt.legend()
        plt.savefig(noExt(args.output,'.txt') + '.png')

    return

# Removes the extension name from a filename if present
def noExt(filename, extensionName):
    if filename[-len(extensionName):].find(extensionName) != -1:
        return filename[:-len(extensionName)]
    return filename


if ( __name__ == '__main__' ):
    main()
