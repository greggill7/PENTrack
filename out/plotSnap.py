#!/usr/bin/env python
# Makes plots from snapshotlog files

def main():
    import numpy as np
    import argparse
    import matplotlib.pyplot as plt

    nbins = 200
    time = []
    endProj = []    # 2d array (# of time elements by # particles)

    parser = argparse.ArgumentParser(description='Makes plots related to neutronsnapshot.out')
    parser.add_argument("-f", "--file", type=str, help = "Filename (default 000000000000neutronsnapshot.out)")
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")
    if (args.proj == False and args.t2 == False):
        print("Missing flags. See [--help]")
        return

    if (args.file):
        filename = args.file
    else:
        filename = '000000000000neutronsnapshot.out'

    try:
        with open (filename,"r") as f1:
            lines = f1.readlines()[1:]
            for num, line in enumerate(lines):
                text = line.split()
                tEnd = float( text[18])
                sxE = float( text[26])
                syE = float( text[27])
                szE = float( text[28])
                bxE = float( text[32])
                byE = float( text[33])
                bzE = float( text[34])

                # This makes it so that time is a list with elements [0,... final time]
                # and endProj is a list of {[particle 1 @ t0, particle 2 @ t0 ...], [particle 1 @ t1, particle 2 @ t1, ...], ...}
                if not time or (tEnd > time[-1]):
                    time.append(tEnd)
                    endProj.append([])
                endProj[ time.index(tEnd) ].append( (sxE*bxE + syE*byE + szE*bzE)/norm(bxE, byE, bzE))

    except IOError:
        print("Error reading ", filename)
        return

    for end, t in zip(endProj, time):
        fig, ax = plt.subplots()
        ax.hist(end, range = [-1,1], bins = nbins)
        ax.set_xlabel('Spin projection of S on B')
        ax.set_ylabel('Number of neutrons')
        ax.set_title('Polarization at t = '+ str(t) + "[s]")
        plt.savefig("endPol_t=" + str(t) + ".png")
        plt.close()
        plt.clf()


    plt.show()

    return

def norm (x, y, z):
    #Finds norm of cartesian vector components
    import numpy as np
    return np.sqrt(x*x + y*y + z*z)

if ( __name__ == '__main__' ):
    main()
