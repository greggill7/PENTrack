#!/usr/bin/env python
# Calcs t2 from neutronspin.out files, examines Sx component falling
# out of sync

T2RANGE = [5, 180]      # Time range [sec] to examine T2
T2RANGE_STEP = 1

def main():
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse
    from scipy.interpolate import interp1d
    from scipy.interpolate import InterpolatedUnivariateSpline

    parser = argparse.ArgumentParser(description="Plot everything related to spin.out files")
    parser.add_argument("-f", "--file", type=str, help = "Filename (default 000000000000neutronspin.out)", default='000000000000neutronspin.out')
    args = parser.parse_args()

    filename = args.file

    # Read in file
    try:
        print("Reading file...")
        num, t, sx = np.loadtxt(filename, skiprows=1, usecols=(1, 2, 6), unpack=True)
    except OSError:
        print("Could not find ", filename)
        return

    totalN = int(num[-1])
    print("Neutrons in file: ",totalN)

    if totalN < 2:
        print("Needs more than 1 neutron in  file")
        return

    # Rearrange sx and t into 2D so that it goes
    # [[sx1_neutron1, sx2_neutron1... ], [sx1_neutron2, sx2_neutron2...]]
    splitIndices = np.searchsorted(num, np.arange(2, totalN + 1))
    sx = np.split(sx, splitIndices)
    t = np.split(t, splitIndices)

    print("Interperolating spin tracking...")
    # Spline interpolate each set of sx for neutrons
    # Obtain a set of sx values for each value in T2RANGE
    t2Times = np.arange(T2RANGE[0],T2RANGE[1],T2RANGE_STEP)
    sxT2 = []
    for t_i, sx_i in zip(t, sx):
        func = InterpolatedUnivariateSpline(t_i, sx_i)
        sxT2.append( func(t2Times) )

    print("Calculating T2")

    # Find std deviation for sx set
    sxT2 = np.transpose(sxT2)
    sxDev = []
    for sxSet in sxT2:
        sxDev.append( np.std(sxSet) )

    # Plotting for sanity check
    fig = plt.figure()
    plt.plot(t2Times, sxDev)
    plt.grid(True)
    plt.title('$\sigma$(Sx) over time')
    plt.xlabel('t [s]')
    plt.ylabel('$\sigma$')
    plt.show()
    return


if ( __name__ == '__main__' ):
    main()
