import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

filename = 'PPM_lanl.txt'
comsolFile = 'ppmCutLine.txt'
comsolFile2 = 'ppmComsol.txt'

df = pd.read_csv(filename, delim_whitespace=True, usecols=[0,1,2,3], names=['z','r','Bz','Br'], comment='#')

# Units from cm and G to m and T
df['r'] = df['r']/100
df['z'] = df['z']/100
df['Bz'] = df['Bz']/10000
df['Br'] = df['Br']/10000

plt.figure()
plt.quiver(df['r'], df['z'], df['Br'], df['Bz'], scale_units='dots', scale=0.1)
plt.xlabel('r [m]')
plt.ylabel('z [m]')

# Now only looking at central axis of PPM
fig, ax = plt.subplots()
df = df.query('r==0')
df.plot('z',['Bz'],grid=True, ax=ax,legend=False)

# # Analytical finite solenoid, central axis
# nI = 100* 100000   # current-turns
# x1 = -0.25    # where solenoid starts [m]
# x2 = 0.25   # where solenoid ends [m]
# mu0 = 4 * np.pi * 10**-7
# rad = 0.1  # radius of coil [m]
#
#
# # Fit a horrible solution
# def function(x, x1, x2, nI):
#     return mu0 * nI /2 * ( (x-x1 / np.sqrt((x-x1)**2 + rad**2)) - (x-x2 / np.sqrt((x-x2)**2 + rad**2))  )
#
# popt, pcov = curve_fit(function, df['z'], df['Bz'], p0 = [x1, x2, nI])
#
# x = np.linspace(df['z'].min(),df['z'].max(),1000)
# plt.plot(x, function(x, *popt), label='analytical')
#
# print("### Fitted parameters ###")
# print('x1[m]\tx2[m]\tnI[A-turns]\trad[m]')
# for value in np.round_(popt,decimals=3):
#     print(value, end="\t")
# print(rad)


# Comsol vector field
df = pd.read_csv(comsolFile2, delim_whitespace=True, usecols=[0,1,2,3,4,5], names=['x','y','z','Bx','By','Bz'], comment='%')
df.query('y==0 and z==0').plot('x',['Bx'],ax=ax, legend=False)
ax.legend(['given', 'comsol'])
plt.title('Field along beam line')
plt.xlabel('x [m]')
plt.ylabel('[T]')

df = df.query('z==0')
plt.figure()
plt.quiver(df['y'], df['x'], df['By'], df['Bx'], scale_units='dots', scale=0.1)
plt.xlabel('r [m]')
plt.ylabel('z [m]')


# # PPM ramp 0-6 T
# neutronCount = [1888, 1768, 1525, 1283, 1074, 983, 858, 858, 869, 869]
# bField = np.linspace(0,6,10, endpoint=True)
# plt.figure()
# plt.xlabel('B [T]')
# plt.ylabel('Neutrons')
# plt.plot(bField, neutronCount, marker='.')
# plt.grid()
plt.show()
