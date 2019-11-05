#!/usr/bin/env python
# Makes plots from neutronend.out files

def main():
    import numpy as np
    import argparse
    import pandas as pd
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    parser = argparse.ArgumentParser(description='Plots neutronend.out histograms')
    parser.add_argument("-f", "--file", type=str, default='000000000000neutronend.out', help = "Filename (default 000000000000neutronend.out)")
    parser.add_argument("-p", "--polarization", action="store_true", help = "Plots end polarization of neutrons")
    parser.add_argument("-e", "--energy", action="store_true", help = "Plots histogram of E_start and velocity distribution")
    parser.add_argument("-t", "--tend", action="store_true", help = "Plots histogram of tend")
    parser.add_argument("-s", "--save", action="store_true", help = "Saves histograms to images")
    parser.add_argument("-xyz", "--xyz", action="store_true", help = "Plots end position of neutrons")
    parser.add_argument("-q", "--query", type=str, help = "User defined query to limit neutrons in histogram", default="all")
    parser.add_argument("-nbins", "--nbins", type=int, help = "Number of bins in histogram (default 200)", default=200)
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")

    df = pd.read_csv(args.file, delim_whitespace=True)# usecols=[1,6,7,8,10,11,12,14,18,19,20,21,26,27,28,32,33,34])
    print("Number of neutrons simulated: ", len(df.index))
    if args.query != "all":
        # Queries may involve any property listed below:
        # ['particle', 'vxstart', 'vystart', 'vzstart', 'Sxstart', 'Systart', 'Szstart', 'Estart', 'tend', 'xend', 'yend', 'zend',
        # 'Sxend', 'Syend', 'Szend', 'BxEnd', 'ByEnd', 'BzEnd']
        df = df.query(args.query)
        print("Number of neutrons after query: ", len(df.index))

    if args.polarization:
        # Find projection of S vector (unit vector) onto B vector (not unit vector)
        endPol = (df['Sxend']*df['BxEnd'] + df['Syend']*df['ByEnd'] + df['Szend']*df['BzEnd'])/np.sqrt(df['BxEnd']**2 + df['ByEnd']**2 + df['BzEnd']**2)
        hist, binEdges = np.histogram(endPol,range = [-1,1], bins = args.nbins)

        # Output total neutrons counted and the average
        print("Total neutrons in histogram: ", int(np.sum(hist)))
        print("Number of NA endPol values: ", endPol.isna().sum())
        print("Av Sz end: ", df['Szend'].mean())
        print("Av Bz end: ", df['BzEnd'].mean())
        print("Av endPol: ", endPol.mean())


        fig, ax = plt.subplots()
        ax.bar(binEdges[1:]-0.005,hist,width=0.01)
        ax.set_xlabel('Spin projection of S on B')
        ax.set_xlim([-1.005,1.005])
        ax.set_ylabel('Number of neutrons')

        if (args.save):
            plt.savefig("endPol.png")

    if (args.xyz):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title("Ending positions")
        ax.scatter(df['xend'], df['yend'], df['zend'])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        # ax.set_xlim3d(-0.15,2.1)
        # ax.set_ylim3d(-.04,.04)
        # ax.set_zlim3d(-.04,.04)

        df.hist('zend', bins = args.nbins, grid=False)
        plt.ylabel('Number of neutrons')
        plt.xlabel('z_end [m]')

    if (args.energy):
        df.hist('Estart', bins = args.nbins, grid=False)
        plt.ylabel('Number of neutrons')
        plt.xlabel('E [eV]')

        if (args.save):
            plt.savefig("startEnergy.png")

        # df.hist('vxstart', bins = args.nbins)
        # plt.ylabel('Number of neutrons')
        # plt.xlabel('[m/s]')
        #
        # df.hist('vystart', bins = args.nbins)
        # plt.ylabel('Number of neutrons')
        # plt.xlabel('[m/s]')
        #
        # df.hist('vzstart', bins = args.nbins)
        # plt.ylabel('Number of neutrons')
        # plt.xlabel('[m/s]')

        # vr, vtheta, vphi = toSpherical(df['vxstart'], df['vystart'], df['vzstart'])
        # histTotal, binEdges = np.histogram(vphi, bins = args.nbins)
        # fig, ax = plt.subplots()
        # ax.bar(binEdges[1:]-0.005,histTotal,width=0.02)
        # ax.set_xlabel(r'$v_\phi$ distribution')
        # ax.set_ylabel('Number of neutrons')
        #
        # fig, ax = plt.subplots()
        # histTotal, binEdges = np.histogram(vtheta, bins = args.nbins)
        # ax.bar(binEdges[1:]-0.005,histTotal,width=0.02)
        # ax.set_xlabel(r'$v_\theta$ distribution')
        # ax.set_ylabel('Number of neutrons')

    if (args.tend):
        df.hist('tend', bins = args.nbins, grid=False)
        plt.ylabel('Number of neutrons')
        plt.xlabel('tend [s]')

        if (args.save):
            plt.savefig("tend.png")


    plt.show()

    return

def toSpherical(x, y, z):
    import numpy as np
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arctan2(y, x)
    theta = np.arccos(np.array(z)/r)
    return r, theta, phi

if ( __name__ == '__main__' ):
    main()
