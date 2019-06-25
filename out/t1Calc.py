#!/usr/bin/env python
# Calcs t1 from neutronspin.out files, examines Sz component falling
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
    parser = argparse.ArgumentParser(description="Calculates T1 from multiple neutronspin.out files")
    parser.add_argument("-r", "--runs", type=int, nargs=2, required=True, help="Start and end values of PENTrack runs")
    parser.add_argument("-f", "--folder", type=str, help = "Folder location (default ./)", default="./")
    parser.add_argument("-t", "--time", type=float, nargs=2, required=True, help="Start and end values of T1 precession time")
    parser.add_argument("-s", "--step", type=float, nargs=1, required=True, help="Step size in [range] with which to calculate T1")
    parser.add_argument("-o", "--output", type=str, help = "Output file name of fit and <Sz>. If file name already exists, reads from file, and ignores -r -f -t -s")
    args = parser.parse_args()

    if args.output:
        exists = os.path.isfile(args.output)
    else:
        exists = False

    if exists:
        # Read <Sz> from pre-existing file
        print("Reading from ", args.output)
        t1Times, szAv = np.genfromtxt(args.output, unpack=True)
    else:

        if (args.folder[-1] != "/"):
            folder = args.folder + "/"
        else:
            folder = args.folder

        print("Reading files and processing...")
        runNum = np.arange(args.runs[0],args.runs[1]+1)
        t1Times = np.arange(args.time[0],args.time[1] + args.step[0],args.step[0])
        simTotal = 0
        missedRuns = []
        # szT1 = []
        szT1 = np.zeros(len(t1Times))


        for i in runNum:
            runName = folder + str(i).zfill(12) + "neutronspin.out"
            print(i,"...", end="")
            sys.stdout.flush()      # Yes, I know print has a flush=True option. Doesn't work in python2
            try:
                df = pd.read_csv(runName, delim_whitespace=True, usecols=[1, 2, 8]).drop_duplicates(subset='t', keep='first')
                # Columns are titled "particle, t, Sz"
            except:
                missedRuns.append(i)
                continue

            simTotal += df["particle"].iloc[-1]

            for particleNum in np.arange(1, df["particle"].iloc[-1] + 1 ):
                interp = InterpolatedUnivariateSpline(df.query("particle == @particleNum")["t"], df.query("particle == @particleNum")["Sz"])
                # szT1.append( interp(t1Times) )
                szT1 = szT1 + np.array( interp(t1Times) )

        print("Done")
        print("\nError reading run numbers-- ", missedRuns)
        print("Number of neutrons simulated: ", simTotal)

        # Find average for sx set
        # szAv = np.mean(szT2, axis=0, dtype=np.float64)
        szAv = szT1/simTotal

        if args.output:
            print("Saving t1Times, <Sz> to ", args.output)
            np.savetxt(args.output, np.c_[t1Times, szAv])

    # Fit function for T2
    print("\nFitting function:")
    print("np.exp(-(t - c) / b )")
    print("Guessed parameters (edit in file)")
    print("[b,c]")
    print(guess)

    popt, pcov = curve_fit(fit, t1Times, szAv, p0=guess)
    print("Fitted parameters")
    print(popt)
    print("+/- [",np.sqrt(pcov[0][0]),", ", np.sqrt(pcov[1][1]), "]")

    # Plotting
    print("\nPlotting...")
    fig = plt.figure()
    plt.plot(t1Times, szAv,color='C0', label="<sz>")
    plt.plot(t1Times, fit(t1Times, *popt), color='C1', label="Fit")
    plt.grid(True)
    plt.xlabel('t [s]')
    plt.ylabel('<Sz>')

    plt.legend()

    if args.output:
        plt.savefig(noExt(args.output,'.txt') + '.png')

    return

# Removes the extension name from a filename if present
def noExt(filename, extensionName):
    if filename[-len(extensionName):].find(extensionName) != -1:
        return filename[:-len(extensionName)]
    return filename

if ( __name__ == '__main__' ):
    main()
