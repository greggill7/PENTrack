#!/usr/bin/env python
# Makes plots from neutronend.out files

def main():
    import numpy as np
    import argparse
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    nbins = 200

    parser = argparse.ArgumentParser(description='Plots neutronend.out histograms')
    parser.add_argument("-f", "--file", type=str, default='000000000000neutronend.out', help = "Filename (default 000000000000neutronend.out)")
    parser.add_argument("-p", "--polarization", action="store_true", help = "Plots end polarization of neutrons")
    parser.add_argument("-e", "--energy", action="store_true", help = "Plots histogram of E_start")
    parser.add_argument("-s", "--save", action="store_true", help = "Saves histograms to images")
    parser.add_argument("-pos", "--position", action="store_true", help = "Plots end position of neutrons in 3D space")
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")

    particle, vxStart, vyStart, vzStart, sxStart, syStart, szStart, Estart, xEnd, yEnd, zEnd, sxEnd, syEnd, szEnd, bxEnd, byEnd, bzEnd = np.genfromtxt(args.file, skip_header=1, unpack=True, usecols=[1,6,7,8,10,11,12,14,19,20,21,26,27,28,32,33,34])

    if args.polarization:
        # Find projection of S vector (unit vector) onto B vector (not unit vector)
        endProj = []        # Projection of S_end onto B_end for multiple neutrons
        for bxE, byE, bzE, sxE, syE, szE in zip (bxEnd, byEnd, bzEnd, sxEnd, syEnd, szEnd):
            if norm(bxE,byE,bzE) == 0:
                continue
            endProj.append( (sxE*bxE + syE*byE + szE*bzE)/norm(bxE, byE, bzE) )

        # Output total neutrons counted and the average
        print("Total neutrons in simulation: ", particle[-1])
        print("Total neutrons in histogram: ", len(endProj))
        print("Av Sz end: ", np.average(szEnd))
        print("Av Bz end: ", np.average(bzEnd))
        print("Average polarization: ", np.average(endProj))

        fig, ax = plt.subplots()
        ax.hist(endProj,range = [-1,1], bins = nbins)
        ax.set_xlabel('Spin projection of S on B')
        ax.set_ylabel('Number of neutrons')

        if (args.save):
            plt.savefig("endPol.png")

    if (args.position):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title("Ending positions")
        ax.scatter(xEnd, yEnd, zEnd)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        # ax.set_xlim3d(-0.15,2.1)
        # ax.set_ylim3d(-.04,.04)
        # ax.set_zlim3d(-.04,.04)

    if (args.energy):
        fig = plt.figure()
        plt.hist(Estart,range = [np.amin(Estart), np.amax(Estart)], bins = 200)
        plt.ylabel('Number of neutrons')
        plt.xlabel('E [eV]')

        if (args.save):
            plt.savefig("startEnergy.png")

        fig = plt.figure()
        plt.hist(vxStart,range = [np.amin(vxStart), np.amax(vxStart)], bins = 200)
        plt.ylabel('Number of neutrons')
        plt.xlabel('vx_start [m/s]')

        fig = plt.figure()
        plt.hist(vyStart,range = [np.amin(vyStart), np.amax(vyStart)], bins = 200)
        plt.ylabel('Number of neutrons')
        plt.xlabel('vy_start [m/s]')

        fig = plt.figure()
        plt.hist(vyStart,range = [np.amin(vzStart), np.amax(vzStart)], bins = 200)
        plt.ylabel('Number of neutrons')
        plt.xlabel('vz_start [m/s]')

    plt.show()

    return

def norm (x, y, z):
    #Finds norm of cartesian vector components
    import numpy as np
    return np.sqrt(x*x + y*y + z*z)

if ( __name__ == '__main__' ):
    main()
