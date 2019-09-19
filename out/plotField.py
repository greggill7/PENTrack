#!/usr/bin/env python
# Plots xz plane in BFcut.out
def main():
    import matplotlib.pyplot as plt
    import argparse
    import numpy as np

    x = []
    y = []
    z = []
    bx = []
    by = []
    bz = []
    bNorm = []
    xTemp = []
    yTemp = []

    parser = argparse.ArgumentParser(description='Plots BFcut.out [--help]')
    parser.add_argument("-f", "--file", type=str, default='BFCut.out', help = "Filename (default BFCut.out)")
    parser.add_argument("-xz", "--xzPlane", action="store_true", help = "Plots BFCut along xz plane")
    parser.add_argument("-yz", "--yzPlane", action="store_true", help = "Plots BFCut along yz plane")
    parser.add_argument("-n", "--norm", type=float, nargs=1, help = "Plots the flux norm along an arc length, fixed z")
    parser.add_argument("-a", "--adiab", action="store_true", help = "If --norm enabled, plots adiabaticity")
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")
    if (args.xzPlane == False and args.yzPlane == False):
        print("Please specify which plane you'd like to plot [--help]")
        return

    # Read in files
    try:
        with open (args.file,"r") as f1:
            lines = f1.readlines()[1:]
            for num, line in enumerate(lines):
                text = line.split(' ')
                if (len(text) == 3):
                    x.append(float( text[0]) )
                    y.append(float( text[1]) )
                    z.append(float( text[2]) )
                else:
                    bx.append(float( text[0]) )
                    by.append(float( text[4]) )
                    bz.append(float( text[8]) )
    except IOError:
        print("Error reading ", args.file)
        return

    if (len(x) != len(bx)):
        print("Error: not an equal number of xyz coords and b field values")
        return

    if args.xzPlane:
        fig = plt.figure()
        plt.quiver(x[::5], z[::5], bx[::5], bz[::5], units='x')
        plt.title('Vector Field xz plane')

        if args.norm:
            for b1, b2, b3, x0, z0 in zip(bx, by, bz, x, z):
                if z0 == args.norm[0]:
                    xTemp.append(x0)
                    bNorm.append( norm(b1, b2, b3) )
            if not bNorm:
                print("Error: BNorm plot empty (Cut line z = ", args.norm, ")")
                return

            if args.adiab:
                k = calcAdiab(x, bx, by, bz)
                nonAdiab = 1./ np.array(k)
                plt.figure()
                plt.plot(x[0:-2], k, label='k')
                plt.xlabel('[m]')
                plt.yscale('log')
                plt.legend()
                plt.grid()

                plt.figure()
                plt.plot(x[0:-2], nonAdiab, label='1/k')
                plt.xlabel('[m]')
                plt.legend()
                plt.grid()

        plt.figure()
        plt.plot(x, bx, label=r'$B_x$')
        plt.plot(x, by, label=r'$B_y$')
        plt.plot(x, bz, label=r'$B_z$')
        plt.plot(x, bNorm, label=r'$\Vert B \Vert$')
        plt.ylabel('[Tesla]')
        plt.xlabel('[m]')
        plt.legend()
        plt.grid()



    if args.yzPlane:
        fig = plt.figure()
        plt.quiver(y[::5], z[::5], by[::5], bz[::5], units='x')
        plt.title('Vector Field yz plane')

        if args.norm:
            for b1, b2, b3, y0, z0 in zip(bx, by, bz, y, z):
                if z0 == args.norm[0]:
                    yTemp.append(y0)
                    bNorm.append( norm(b1, b2, b3) )
            if not bNorm:
                print("BNorm plot empty (Cut line z = ", args.norm, ")")

            if args.adiab:
                k = calcAdiab(y, by, bx, bz)
                nonAdiab = 1./ np.array(k)
                nonAdiab = 1./ np.array(k)
                plt.figure()
                plt.plot(x[0:-2], k, label='k')
                plt.xlabel('[m]')
                plt.yscale('log')
                plt.legend()
                plt.grid()

                plt.figure()
                plt.plot(x[0:-2], nonAdiab, label='1/k')
                plt.xlabel('[m]')
                plt.legend()
                plt.grid()

            plt.figure()
            plt.plot(x, bx, label=r'$B_x$')
            plt.plot(x, by, label=r'$B_y$')
            plt.plot(x, bz, label=r'$B_z$')
            plt.plot(x, bNorm, label=r'$\Vert B \Vert$')
            plt.ylabel('[Tesla]')
            plt.xlabel('[m]')
            plt.legend()
            plt.grid()

    plt.show()

    return

def calcAdiab(x, bx, by , bz):
    # x -> direction of travel for the neutron
    import numpy as np
    bx = np.array(bx)
    by = np.array(by)
    bz = np.array(bz)
    x = np.array(x)
    gamma_n = 30* 10**6 # Hz/T
    vn = 4              # m/s
    Btotals = np.sqrt(bx**2 + by**2 + bz**2)
    B1dotB2 = bx[0:-2]*bx[1:-1] + by[0:-2]*by[1:-1] + bz[0:-2]*bz[1:-1]
    k = gamma_n*((Btotals[0:-2] + Btotals[1:-1])/2.)*np.abs(x[1:-1] - x[0:-2])/(vn*np.arccos(B1dotB2/(Btotals[0:-2]*Btotals[1:-1])))
    return k


def norm (x, y, z):
    #Finds norm of cartesian vector components
    import numpy as np
    return np.sqrt(x*x + y*y + z*z)

if ( __name__ == '__main__' ):
    main()
