#!/usr/bin/env python
# Makes plots from neutronspin.out files

def main():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import argparse
    import h5py

    yNeutron = 1.83247172e8 / 6.28318530718 # s^-1 T^-1. For adiabatic parameter calculation
    adiab = []

    parser = argparse.ArgumentParser(description='Plot everything related to spin.out files')
    parser.add_argument('-f', '--file', type=str, default='000000000000neutronspin.out', help = 'Filename (default 000000000000neutronspin.out)')
    parser.add_argument('-q', '--query', type=str, help = 'User defined query to limit neutrons in histogram')
    parser.add_argument('-hdf', '--hdf', type=str, help='Read an hdf file instead of text')
    parser.add_argument('-w', '--where', type=str, help='If [--hdf] is enabled, can query while reading in the file')
    parser.add_argument('-p', '--proj', action='store_true', help = 'Spin projection plots')
    parser.add_argument('-s', '--spin', action='store_true', help = 'sx, sy, sz plots')
    parser.add_argument('-a', '--adiab', action='store_true', help = 'Finds adiabaticity (dB/dt)/(y B^2)')
    parser.add_argument('-four', '--fourier', action='store_true', help = 'Prints fourier transform of spin components')
    parser.add_argument('-td', '--threeD', action='store_true', help = '3d plot of spin vector')
    args = parser.parse_args()

    print('Reminder: Use --help or -h to see optional arguments')
    print('Reading file')

    if args.hdf == None:
        df = pd.read_csv(args.file, delim_whitespace=True)
    else:
        with h5py.File( args.hdf, "r") as hdfInFile:
            # key=hdfInFile.keys()[0]  # For python2
            key = list( hdfInFile.keys() )[0]
        if args.where == None:
            df = pd.read_hdf(args.hdf, key)
        else:
            df = pd.read_hdf(args.hdf, key, where=[args.where])

    if args.query != None:
        df = df.query(args.query)

    # # Make additional cuts here...
    # for particleNum in df['particle'].unique():
    #     if (df.query('particle== @particleNum')['x'].iloc[-1] > 0) or (particleNum in [39,41,77,81,93] ) or (not df.query('particle==@particleNum and x>2.17').empty):
    #         df.drop( df[ df.particle == particleNum ].index, inplace=True)
    #         print('Cutting neutron ', particleNum)

    # # # Calculate spin projection on magnetic fields
    np.seterr(divide='ignore', invalid='ignore')    # Ignore divide by 0 warnings
    df['bNorm'] = np.sqrt(df['Bx']**2 + df['By']**2 + df['Bz']**2)
    df['proj'] = (df['Sx']*df['Bx'] + df['Sy']*df['By'] + df['Sz']*df['Bz'])/df['bNorm']

    # Calculate adiabatic parameter for a given neutron
    # (dB/dt)/(y B^2)
    if args.adiab:
        for i in range(1,len(df.index)):
            adiab.append(( np.abs(df['bNorm'].iloc[i]-df['bNorm'].iloc[i-1])/(df['t'].iloc[i]-df['t'].iloc[i-1]))/ (yNeutron * df['bNorm'].iloc[i]**2))

    # # PLOT STUFF #
    print('Plotting...')
    if (args.proj):
        fig = plt.figure()
        plt.plot(df['x'], df['proj'], '.',markersize=0.5)
        plt.grid(True)
        plt.title('x vs Spin Proj')
        plt.xlabel('x [m]')
        plt.ylabel('Projection of S on B')

        fig = plt.figure()
        plt.plot(df['t'], df['proj'], '.',markersize=0.5)
        plt.grid(True)
        plt.title('t vs Spin Proj')
        plt.xlabel('t [s]')
        plt.ylabel('Projection of S on B')

        fig = plt.figure()
        plt.plot(df['t'], df['x'], '.',markersize=0.5)
        plt.grid(True)
        plt.title('time vs position')
        plt.xlabel('t [s]')
        plt.ylabel('x [m]')

    if (args.spin):
        fig = plt.figure()
        plt.plot(df['x'], df['Sx'])
        plt.grid(True)
        plt.title('Sx(x)')
        plt.xlabel('x [m]')
        plt.ylabel('P(x)')

        fig = plt.figure()
        plt.plot(df['x'], df['Sy'])
        plt.grid(True)
        plt.title('Sy(x)')
        plt.xlabel('x [m]')
        plt.ylabel('P(y)')

        fig = plt.figure()
        plt.plot(df['x'], df['Sz'], '.',markersize=0.5)
        plt.grid(True)
        plt.title('Sz(x)')
        plt.xlabel('x [m]')
        plt.ylabel('P(z)')

        fig = plt.figure()
        plt.plot(df['t'], df['Sx'])
        plt.grid(True)
        plt.title('Sx(t)')
        plt.xlabel('t [s]')
        plt.ylabel('P(x)')

        fig = plt.figure()
        plt.plot(df['t'], df['Sy'])
        plt.grid(True)
        plt.title('Sy(t)')
        plt.xlabel('t [s]')
        plt.ylabel('P(y)')

        fig = plt.figure()
        plt.plot(df['t'], df['Sz'])
        plt.grid(True)
        plt.title('Sz(t)')
        plt.xlabel('t [s]')
        plt.ylabel('P(z)')

    if (args.adiab):
        fig = plt.figure()
        plt.plot(df['t'].tolist()[1:], adiab)
        plt.yscale('log')
        plt.grid(True)
        plt.title('Adiabatic parameter')
        # plt.ylim(-5,5)
        plt.xlabel('t [sec]')
        plt.ylabel('k')

    if (args.fourier):        # Fourier transform graphs
        # Calculate fourier transform of oscillation in Sx Sy Sz
        timestep = df['t'].iloc[-1]/len(df.index)
        fourSx = np.fft.fft(df['Sx'].tolist())
        fourSy = np.fft.fft(df['Sy'].tolist())
        fourSz = np.fft.fft(df['Sz'].tolist())
        freq = np.fft.fftfreq( len(df.index), d=timestep )

        fig = plt.figure()
        plt.plot(freq, np.abs(fourSy) )
        plt.grid(True)
        plt.xlabel('[Hz]')
        plt.title('Fourier transform of Sy')

        fig = plt.figure()
        plt.plot(freq, np.abs(fourSz) )
        plt.grid(True)
        plt.xlabel('[Hz]')
        plt.title('Fourier transform of Sz')

        fig = plt.figure()
        plt.plot(freq, np.abs(fourSx) )
        plt.grid(True)
        plt.xlabel('[Hz]')
        plt.title('Fourier transform of Sx')

    if (args.threeD):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title('(Semi classical) Spin')
        ax.scatter(df['Sx'], df['Sy'], df['Sz'])
        ax.set_xlim3d(-1,1)
        ax.set_ylim3d(-1,1)
        ax.set_zlim3d(-1,1)
        ax.set_xlabel('Sx')
        ax.set_ylabel('Sy')
        ax.set_zlabel('Sz')
        ax.view_init(30,220)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title('Neutron Trajectory')
        ax.scatter(df['x'], df['y'], df['z'])
        # ax.set_xlim3d(-1,1)
        # ax.set_ylim3d(-1,1)
        # ax.set_zlim3d(-1,1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.view_init(30,220)


    plt.show()

    return

if ( __name__ == '__main__' ):
    main()
