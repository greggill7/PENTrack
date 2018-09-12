guideTest4
===========================

This is Chris Cude's model of a segmented solenoid inside a mumetal shielded
housing

The cylinder goes from z= -2 to z =0. Neutrons start at z = -2).
Radius is 1.5*0.0254. y=-0.127

Unfortunately, PENTrack requires that gravity be in the z direction,
so I've flipped the coordinates of the x-->y, y-->z, z-->x in the vector field file using
changeColumns.py

So, corrected, the cylinder goes from x= -2 to x =-0. Neutrons start at x = -2

Radius is 1.5*0.0254. z=-0.127

Run the test with ./RunTest.sh
