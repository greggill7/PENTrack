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
    parser.add_argument("-s", "--save", action="store_true", help = "Saves histogram to endPol.png")
    parser.add_argument("-pos", "--position", action="store_true", help = "Plots end position of neutrons")
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")

    particle, sxStart, syStart, szStart, xEnd, yEnd, zEnd, sxEnd, syEnd, szEnd, bxEnd, byEnd, bzEnd = np.genfromtxt(args.file, skip_header=1, unpack=True, usecols=[1,10,11,12,19,20,21,26,27,28,32,33,34])

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
    ax.set_title('Polarization of neutrons at end')


    if (args.save):
        plt.savefig("endPol.png")

    if (args.position):
        fig2 = plt.figure(2)
        ax2 = fig2.add_subplot(111, projection='3d')
        plt.title("Ending positions")
        ax2.scatter(xEnd, yEnd, zEnd)
        ax2.set_xlabel("x")
        ax2.set_ylabel("y")
        ax2.set_zlabel("z")

    plt.show()

    return

def norm (x, y, z):
    #Finds norm of cartesian vector components
    import numpy as np
    return np.sqrt(x*x + y*y + z*z)

if ( __name__ == '__main__' ):
    main()
