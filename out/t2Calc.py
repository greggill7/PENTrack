#!/usr/bin/env python
# Calcs t2 from neutronspin.out files, examines Sx component falling
# out of sync

#from __future__ import print_function

def main():
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse
    import pandas as pd
    from scipy.interpolate import InterpolatedUnivariateSpline
    # import sys

    parser = argparse.ArgumentParser(description="Calculates T2 from multiple neutronspin.out files")
    parser.add_argument("-r", "--runs", type=int, nargs=2, required=True, help="Start and end values of PENTrack runs")
    parser.add_argument("-f", "--folder", type=str, help = "Folder location (default ./)", default="./")
    parser.add_argument("-t", "--time", type=float, nargs=2, required=True, help="Start and end values of T2 precession time")
    parser.add_argument("-s", "--step", type=float, nargs=1, required=True, help="Step size in [range] with which to calculate T2")
    args = parser.parse_args()


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
        print(int(progress/float(len(runNum))*100),"%...", end="", flush=True) # Flush doesn't work in python 2
        progress += 1
        # sys.stdout.flush()
        try:
            df = pd.read_csv(runName, delim_whitespace=True, usecols=[1, 2, 6])
            # Columns are titled "particle, t, Sx"
        except:
            missedRuns.append(i)
            continue

        simTotal += df["particle"].iloc[-1] - df["particle"].iloc[0]

        for particleNum in np.arange(1, df["particle"].iloc[-1] + 1 ):
            func = InterpolatedUnivariateSpline(df.query("particle == @particleNum")["t"], df.query("particle == @particleNum")["Sx"])
            sxT2.append( func(t2Times) )

    print("100%... Now Plotting")
    print("Error reading run numbers-- ", missedRuns)
    print("Number of neutrons simulated: ", simTotal)

    # Find average for sx set
    sxT2 = np.transpose(sxT2)
    sxAv = []
    sxDev = []
    for sxSet in sxT2:
        sxAv.append( np.average(sxSet) )
        sxDev.append( np.std(sxSet) )

    # Plotting for sanity check
    fig = plt.figure()
    plt.plot(t2Times, sxDev)
    plt.grid(True)
    plt.title('$\sigma$(Sx) over time')
    plt.xlabel('t [s]')
    plt.ylabel('$\sigma$')

    fig = plt.figure()
    plt.plot(t2Times, sxAv)
    plt.grid(True)
    plt.title('<Sx> over time')
    plt.xlabel('t [s]')
    plt.ylabel('<Sx>')

    plt.show()
    return


if ( __name__ == '__main__' ):
    main()
