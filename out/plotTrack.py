#!/usr/bin/env python
# Makes plots from neutrontrack.out files
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import h5py
import uproot

def main():
    yNeutron = 1.83247172e8 / 6.28318530718 # s^-1 T^-1. For adiabatic parameter calculation
    markersize = 1
    adiab = []
    Estart = []

    parser = argparse.ArgumentParser(description='Plot everything related to track.out files')
    parser.add_argument('-f', '--file', type=str, default='000000000000neutrontrack.out', help = 'Text file (default 000000000000neutrontrack.out)')
    parser.add_argument('-q', '--query', type=str, help = 'User defined query to limit neutrons in histogram')
    parser.add_argument('-hdf', '--hdf', type=str, help='Read an hdf file instead of text')
    parser.add_argument('-w', '--where', type=str, help='If [--hdf] is enabled, can query while reading in the file')
    parser.add_argument('-r', '--root', type=str, help = 'Read in a root file')
    parser.add_argument('-xz', '--xz', action='store_true', help = 'Neutron motion in XZ')
    parser.add_argument('-yz', '--yz', action='store_true', help = 'Neutron motion in YZ')
    parser.add_argument('-e', '--energy', action='store_true', help = 'Plots histogram of E_start')
    parser.add_argument('-a', '--adiab', action='store_true', help = 'Finds adiabaticity (dB/dt)/(y B^2)')
    parser.add_argument('-td', '--threeD', action='store_true', help = '3d plot of neutron trajectory')
    args = parser.parse_args()

    print('Reminder: Use --help or -h to see optional arguments')
    print('Reading file')

    if args.hdf:
        with h5py.File( args.hdf, "r") as hdfInFile:
            # key=hdfInFile.keys()[0]  # For python2
            key = list( hdfInFile.keys() )[0]
        if args.where == None:
            df = pd.read_hdf(args.hdf, key)
        else:
            df = pd.read_hdf(args.hdf, key, where=[args.where])
    elif args.root:
        file = uproot.open(args.root)
        df = file['neutrontrack'].pandas.df()
    else:
        df = pd.read_csv(args.file, delim_whitespace=True)

    if args.query != None:
        df = df.query(args.query)

    # # Make additional cuts here...
    # for particleNum in df['particle'].unique():
    #     if (df.query('particle== @particleNum')['x'].iloc[-1] > 0) or (particleNum in [39,41,77,81,93] ) or (not df.query('particle==@particleNum and x>2.17').empty):
    #         df.drop( df[ df.particle == particleNum ].index, inplace=True)
    #         print('Cutting neutron ', particleNum)

    # Calculate adiabatic parameter for a given neutron
    # (dB/dt)/(y B^2)
    if args.adiab:
        np.seterr(divide='ignore', invalid='ignore')    # Ignore divide by 0 warnings
        df['bNorm'] = np.sqrt(df['Bx']**2 + df['By']**2 + df['Bz']**2)
        for i in range(1,len(df.index)):
            adiab.append(( np.abs(df['bNorm'].iloc[i]-df['bNorm'].iloc[i-1])/(df['t'].iloc[i]-df['t'].iloc[i-1]))/ (yNeutron * df['bNorm'].iloc[i]**2))

    # Get starting neutron energy
    if args.energy:
        for particleNum in df['particle'].unique():
            Estart.append(df.query('particle == @particleNum')['E'].iloc[0])

    # # PLOT STUFF #
    print('Plotting...')
    if (args.xz):
        fig = plt.figure()
        plt.plot(df['x'], df['z'], '.',markersize=markersize)
        plt.grid(True)
        plt.xlabel('x [m]')
        plt.ylabel('z [m]')

        fig = plt.figure()
        plt.plot(df['t'], df['x'], '.',markersize=markersize)
        plt.grid(True)
        plt.xlabel('t [s]')
        plt.ylabel('x [m]')

    if (args.yz):
        fig = plt.figure()
        plt.plot(df['y'], df['z'], '.',markersize=markersize)
        plt.grid(True)
        plt.xlabel('y [m]')
        plt.ylabel('z [m]')

        fig = plt.figure()
        plt.plot(df['t'], df['y'], '.',markersize=markersize)
        plt.grid(True)
        plt.xlabel('t [s]')
        plt.ylabel('y [m]')

    if (args.energy):
        fig = plt.figure()
        plt.hist(Estart,range = [0,225E-9], bins = 225)
        plt.ylabel('Number of neutrons')
        plt.xlabel('E [eV]')

    if (args.adiab):
        fig = plt.figure()
        plt.plot(df['t'].tolist()[1:], adiab)
        plt.grid(True)
        plt.yscale('log')
        plt.title('Adiabatic parameter')
        # plt.ylim(-5,5)
        plt.xlabel('t [sec]')
        plt.ylabel('k')

    if (args.threeD):
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
