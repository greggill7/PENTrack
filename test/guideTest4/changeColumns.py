#!/usr/bin/env python

def main():
    import numpy as np

    x = []
    y = []
    z = []
    bx = []
    by = []
    bz = []

    try:
        with open ('cude_field.txt',"r") as f1:
            lines = f1.readlines()[8:]
            for num, line in enumerate(lines):
                text = line.split()

                x.append(float( text[0]) )
                y.append(float( text[1]) )
                z.append(float( text[2]) )
                bx.append(float( text[3]) )
                by.append(float( text[4]) )
                bz.append(float( text[5]) )
    except IOError:
        print("Error reading file")
        return

    np.savetxt("cude_field_columnsFlipped.txt",np.c_[z, x, y, bz, bx, by])
    return


if ( __name__ == '__main__' ):
    main()
