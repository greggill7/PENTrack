#!/usr/bin/env python
# Plots xz plane in BFcut.out
def main():
    import matplotlib.pyplot as plt
    import argparse

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
    parser.add_argument("-f", "--file", type=str, help = "Filename (default BFCut.out)")
    parser.add_argument("-xz", "--xzPlane", action="store_true", help = "Plots BFCut along xz plane")
    parser.add_argument("-yz", "--yzPlane", action="store_true", help = "Plots BFCut along yz plane")
    parser.add_argument("-n", "--norm", type=float, nargs=1, help = "Plots the flux norm along an arc length, fixed z")
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")
    if (args.xzPlane == False and args.yzPlane == False):
        print("Please specify which plane you'd like to plot [--help]")
        return

    if (args.file):
        filename = args.file
    else:
        filename = 'BFCut.out'

    # Read in files
    try:
        with open (filename,"r") as f1:
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
        print("Error reading ", filename)
        return

    if (len(x) != len(bx)):
        print("Error: not an equal number of xyz coords and b field values")
        return

    if args.xzPlane:
        fig1 = plt.figure(1)
        plt.quiver(x[::5], z[::5], bx[::5], bz[::5], units='x')
        plt.title('Vector Field xz plane')

        if args.norm:
            for b1, b2, b3, x0, z0 in zip(bx, by, bz, x, z):
                if z0 == args.norm[0]:
                    xTemp.append(x0)
                    bNorm.append( norm(b1, b2, b3) )

            if not bNorm:
                print("BNorm plot empty (Cut line z = ", args.norm, ")")

            fig2 =  plt.figure(2)
            plt.plot(xTemp, bNorm)
            plt.title('B field norm')
            plt.grid(True)
            plt.xlabel('x [m]')
            plt.ylabel('|B| [T]')

    if args.yzPlane:
        fig3 = plt.figure(3)
        plt.quiver(y[::5], z[::5], by[::5], bz[::5], units='x')
        plt.title('Vector Field yz plane')

        if args.norm:
            for b1, b2, b3, y0, z0 in zip(bx, by, bz, y, z):
                if z0 == args.norm[0]:
                    yTemp.append(y0)
                    bNorm.append( norm(b1, b2, b3) )

            if not bNorm:
                print("BNorm plot empty (Cut line z = ", args.norm, ")")

            fig4 =  plt.figure(4)
            plt.plot(yTemp, bNorm)
            plt.title('B field norm')
            plt.grid(True)
            plt.xlabel('y [m]')
            plt.ylabel('|B| [T]')

    plt.show()

    return

def norm (x, y, z):
    #Finds norm of cartesian vector components
    import numpy as np
    return np.sqrt(x*x + y*y + z*z)

if ( __name__ == '__main__' ):
    main()
