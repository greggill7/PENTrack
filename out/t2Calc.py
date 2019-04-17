#!/usr/bin/env python
# Calcs t2 from neutronspin.out files, examines Sx component falling
# out of sync

#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.optimize import curve_fit
import sys
import os

def fit(t, c, b, w, phi):
    # Function for fitting <Sx>
    return np.exp(-(t - c) / b ) * np.sin(w*t + phi)

# Guess for parameters to fit
guess = [30, 50,183, 807]

def main():
    parser = argparse.ArgumentParser(description="Calculates T2 from multiple neutronspin.out files")
    parser.add_argument("-r", "--runs", type=int, nargs=2, required=True, help="Start and end values of PENTrack runs")
    parser.add_argument("-f", "--folder", type=str, help = "Folder location (default ./)", default="./")
    parser.add_argument("-t", "--time", type=float, nargs=2, required=True, help="Start and end values of T2 precession time")
    parser.add_argument("-s", "--step", type=float, nargs=1, required=True, help="Step size in [range] with which to calculate T2")
    parser.add_argument("-o", "--output", type=str, help = "Output file name of fit and <Sx>. If file name already exists, reads from file, and ignores -r -f -t -s")
    args = parser.parse_args()

    if args.output:
        exists = os.path.isfile(args.output)
    else:
        exists = False

    if exists:
        # Read <Sx> from pre-existing file
        print("Reading from ", args.output)
        t2Times, sxAv = np.genfromtxt(args.output, unpack=True)
    else:

        if (args.folder[-1] != "/"):
            folder = args.folder + "/"
        else:
            folder = args.folder

        print("Reading files and processing...")
        runNum = np.arange(args.runs[0],args.runs[1]+1)
        t2Times = np.arange(args.time[0],args.time[1] + args.step[0],args.step[0])
        simTotal = 0
        progress = 0
        missedRuns = []
        sxT2 = []


        for i in runNum:
            runName = folder + str(i).zfill(12) + "neutronspin.out"
            print(int(progress/float(len(runNum))*100),"%...", end="")
            progress += 1
            sys.stdout.flush()      # Yes, I know print has a flush=True option. Doesn't work in python2
            try:
                df = pd.read_csv(runName, delim_whitespace=True, usecols=[1, 2, 6])
                # Columns are titled "particle, t, Sx"
            except:
                missedRuns.append(i)
                continue

            simTotal += df["particle"].iloc[-1]

            for particleNum in np.arange(1, df["particle"].iloc[-1] + 1 ):
                interp = InterpolatedUnivariateSpline(df.query("particle == @particleNum")["t"], df.query("particle == @particleNum")["Sx"])
                sxT2.append( interp(t2Times) )

        print("100%")
        print("Error reading run numbers-- ", missedRuns)
        print("Number of neutrons simulated: ", simTotal)

        # Find average for sx set
        sxT2 = np.transpose(sxT2)
        sxAv = []
        for sxSet in sxT2:
            sxAv.append( np.average(sxSet) )

        if args.output:
            print("Saving t2Times and <Sx> to ", args.output)
            np.savetxt(args.output, np.c_[t2Times, sxAv])

    # Fit function for T2
    print("\nFitting function:")
    print("exp(-(t - c) / b ) * sin(w*t + phi)")
    print("Guessed parameters (edit in file)")
    print(guess)

    popt, pcov = curve_fit(fit, t2Times, sxAv, p0=guess)
    print("Fitted parameters")
    print(popt)
    print("+/- [",np.sqrt(pcov[0][0]),", ", np.sqrt(pcov[1][1]), ", ", \
            np.sqrt(pcov[2][2]), ", ", np.sqrt(pcov[3][3]), "]")


    # Plotting
    print("\nPlotting...")
    fig = plt.figure()
    plt.plot(t2Times, sxAv,color='C0')
    plt.plot(t2Times, fit(t2Times, *popt), color='C1')
    plt.grid(True)
    plt.title('<Sx> over time')
    plt.xlabel('t [s]')
    plt.ylabel('<Sx>')

    plt.show()
    return


if ( __name__ == '__main__' ):
    main()
