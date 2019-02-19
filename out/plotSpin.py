#!/usr/bin/env python
# Makes plots from neutronspin.out files

def main():
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import argparse

    yNeutron = 1.83247172e8 / 6.28318530718 # s^-1 T^-1. For adiabatic parameter calculation
    nbins = 200                             # number histogram bins
    t2Times = np.arange(4, 185)                      # times to analyze t2
    t2Temp = []
    t = []
    x = []
    y = []
    z = []
    sx = []
    sxT2 = []
    sxDev = []
    sy = []
    sz = []
    wx = []
    wy = []
    wz = []
    bx = []
    by = []
    bz = []
    bNorm = []
    proj = []
    adiab = []

    parser = argparse.ArgumentParser(description="Plot everything related to spin.out files")
    parser.add_argument("-f", "--file", type=str, help = "Filename (default 000000000000neutronspin.out)")
    parser.add_argument("-p", "--proj", action="store_true", help = "Spin projection plots")
    parser.add_argument("-s", "--spin", action="store_true", help = "sx, sy, sz plots")
    parser.add_argument("-n", "--neutron", type=int, help = "Limit plots to one neutron in file")
    parser.add_argument("-a", "--adiab", action="store_true", help = "Finds adiabaticity (needs -n enabled)")
    parser.add_argument("-four", "--fourier", action="store_true", help = "Prints fourier transform of spin components (needs -n enabled)")
    parser.add_argument("-td", "--threeD", action="store_true", help = "3d plot of spin vector (needs -n enabled)")
    args = parser.parse_args()

    print("Reminder: Use --help or -h to see optional arguments")
    if (args.file):
        filename = args.file
    else:
        filename = '000000000000neutronspin.out'

    try:
        with open (filename,"r") as f1:
            lines = f1.readlines()[1:]
            for num, line in enumerate(lines):
                text = line.split()
                if (args.neutron != None) and (args.neutron != int( text[1])):
                    continue
                t.append(float( text[2]) )
                x.append(float( text[3]) )
                y.append(float( text[4]) )
                z.append(float( text[5]) )
                sx.append(float( text[6]) )
                sy.append(float( text[7]) )
                sz.append(float( text[8]) )
                wx.append(float( text[9]) )
                wy.append(float( text[10]) )
                wz.append(float( text[11]) )
                bx.append(float( text[12]) )
                by.append(float( text[13]) )
                bz.append(float( text[14]) )
    except IOError:
        print("Error reading ", filename)
        return

    # Calculate spin projection on magnetic fields
    np.seterr(divide='ignore', invalid='ignore')    # Ignore divide by 0 warnings

    for i, (bxi, byi, bzi, sxi, syi, szi) in enumerate(zip(bx, by, bz, sx, sy, sz)):
        bNorm.append(norm(bxi, byi, bzi))
        proj.append( (sxi*bxi + syi*byi + szi*bzi)/bNorm[i] )
        # Calculate adiabatic parameter for a given neutron
        # (dB/dt)/(y B^2)
        if (args.neutron != None) and (i != 0):
            adiab.append(( np.abs(bNorm[i]-bNorm[i-1])/(t[i]-t[i-1]))/ (yNeutron * bNorm[i]**2))

    # PLOT STUFF #
    if (args.proj):
        fig1 = plt.figure(1)
        plt.plot(x, proj, ".",markersize=0.5)
        plt.grid(True)
        plt.title('x vs Spin Proj')
        plt.xlabel('x [m]')
        plt.ylabel('Projection of S on B')

        fig2 = plt.figure(2)
        plt.plot(t, proj, ".",markersize=0.5)
        plt.grid(True)
        plt.title('t vs Spin Proj')
        plt.xlabel('t [s]')
        plt.ylabel('Projection of S on B')

        fig3 = plt.figure(3)
        plt.plot(t, x, ".",markersize=0.5)
        plt.grid(True)
        plt.title('time vs position')
        plt.xlabel('t [s]')
        plt.ylabel('x [m]')

    if (args.spin):
        fig4 = plt.figure(4)
        plt.plot(x, sx)
        plt.grid(True)
        plt.title('Sx(x)')
        plt.xlabel('x [m]')
        plt.ylabel('P(x)')

        fig5 = plt.figure(5)
        plt.plot(x, sy)
        plt.grid(True)
        plt.title('Sy(x)')
        plt.xlabel('x [m]')
        plt.ylabel('P(y)')

        fig6 = plt.figure(6)
        plt.plot(x, sz, ".",markersize=0.5)
        plt.grid(True)
        plt.title('Sz(x)')
        plt.xlabel('x [m]')
        plt.ylabel('P(z)')

        fig7 = plt.figure(7)
        plt.plot(t, sx)
        plt.grid(True)
        plt.title('Sx(t)')
        plt.xlabel('t [s]')
        plt.ylabel('P(x)')

        fig8 = plt.figure(8)
        plt.plot(t, sy)
        plt.grid(True)
        plt.title('Sy(t)')
        plt.xlabel('t [s]')
        plt.ylabel('P(y)')

        fig9 = plt.figure(9)
        plt.plot(t, sz)
        plt.grid(True)
        plt.title('Sz(t)')
        plt.xlabel('t [s]')
        plt.ylabel('P(z)')

    if (args.neutron):
        if (args.adiab):
            fig10 = plt.figure(10)
            plt.plot(x[1:], adiab)
            plt.grid(True)
            plt.title('Adiabatic parameter')
            # plt.ylim(-5,5)
            plt.xlabel('x [m]')
            plt.ylabel('k')

        if (args.fourier):        # Fourier transform graphs
            # Calculate fourier transform of oscillation in Sy and Sz
            timestep = t[-1]
            fourSx = np.fft.fft(sx)
            fourSy = np.fft.fft(sy)
            fourSz = np.fft.fft(sz)
            freqX = np.fft.fftfreq( len(sx), d=timestep )
            freqY = np.fft.fftfreq( len(sz), d=timestep )
            freqZ = np.fft.fftfreq( len(sz), d=timestep )

            fig11 = plt.figure(11)
            plt.plot(freqY, np.abs(fourSy) )
            plt.grid(True)
            plt.xlabel('[Hz]')
            plt.title('Fourier transform of Sy')

            fig12 = plt.figure(12)
            plt.plot(freqZ, np.abs(fourSz) )
            plt.grid(True)
            plt.xlabel('[Hz]')
            plt.title('Fourier transform of Sz')

            fig13 = plt.figure(13)
            plt.plot(freqX, np.abs(fourSx) )
            plt.grid(True)
            plt.xlabel('[Hz]')
            plt.title('Fourier transform of Sx')

        if (args.threeD):
            fig14 = plt.figure(14)
            ax14 = fig14.add_subplot(111, projection='3d')
            plt.title('(Semi classical) Spin')
            ax14.scatter(sx, sy, sz)
            ax14.set_xlim3d(-1,1)
            ax14.set_ylim3d(-1,1)
            ax14.set_zlim3d(-1,1)
            ax14.set_xlabel('Sx')
            ax14.set_ylabel('Sy')
            ax14.set_zlabel('Sz')
            ax14.view_init(30,220)

    plt.show()

    return

def norm (x, y, z):
    #Finds norm of cartesian vector components
    import numpy as np
    return np.sqrt(x*x + y*y + z*z)

def closestInd(val1, val2, range):
    # Determines if "val1" and "val2" contains some value in the list "range"
    # between them. Assumes val2 > val 1. Returns index in range of the value if true,
    # returns None if false
    import numpy as np
    from bisect import bisect_left

    startInd = bisect_left(range, val1)
    if (startInd == len(range)):
        startInd = startInd - 1

    if ( val1 <= range[startInd] and val2 > range[startInd]):
        return startInd
    else:
        return None

if ( __name__ == '__main__' ):
    main()
