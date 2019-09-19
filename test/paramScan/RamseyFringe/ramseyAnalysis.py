#!/usr/bin/env python
# Makes ramseyfringes from joblist.out and endlogs

def main():
    import numpy as np
    import matplotlib.pyplot as plt

    filenames = []
    wFreq = []

    szAv = []
    wVal = []

    neutronCount = []
    particle= []
    SxStart = []
    SyStart = []
    SzStart = []
    SxEnd = []
    SyEnd = []
    SzEnd = []
    BxEnd = []
    ByEnd = []
    BzEnd = []


    print("Reading joblist.out")

    try:
        with open ('joblist.out',"r") as f:
            lines = f.readlines()
            for line in lines:
                if (line[0]=="#"):      # Skip commented lines
                    continue
                text = line.split()
                filenames.append(text[0])
                wFreq.append(float(text[1]) )
    except IOError:
        print("Error reading joblist.out")
        return

    print("Looking for files " + filenames[0] + " through " + filenames[-1])
    print("Start freq of ramsey fringe: ", wFreq[0])
    print("End freq of ramsey fringe: ", wFreq[-1])

    missedFiles = 0
    for endlog, w in zip(filenames, wFreq):
        try:
            with open (endlog,"r") as f:
                lines = f.readlines()[1:] # Skip first line in endlog
                for line in lines:
                    text = line.split()
                    if len(text) < 34:  # Some jobs aborted
                        break
                    particle.append(int( text[1]) )
                    SxStart.append(float( text[10]) )
                    SyStart.append(float( text[11]) )
                    SzStart.append(float( text[12]) )
                    SxEnd.append(float( text[26]) )
                    SyEnd.append(float( text[27]) )
                    SzEnd.append(float( text[28]) )
                    BxEnd.append(float( text[32]) )
                    ByEnd.append(float( text[33]) )
                    BzEnd.append(float( text[34]) )
                # Save the interesting info
                szAv.append(np.average(SzEnd))
                neutronCount.append(particle[-1])
                wVal.append(w)
                # Clear lists for next iteration
                del particle[:]
                del SxStart[:]
                del SyStart[:]
                del SzStart[:]
                del SxEnd[:]
                del SyEnd[:]
                del SzEnd[:]
                del BxEnd[:]
                del ByEnd[:]
                del BzEnd[:]
        except IOError:
            missedFiles += 1

    # Report basic stuff
    print("Most neutrons found in a file: ", np.amax(neutronCount))
    print("Fewest neutrons found in a file: ", np.amin(neutronCount))
    print("Number of missed/unreadable files: ", missedFiles)
    print("The resonant freq is\t", wVal[szAv.index( min(szAv) )], "rad/s" )

    # Plot stuff
    fig1 = plt.figure(1)
    plt.plot(wVal, szAv, ".")
    plt.grid(True)
    plt.title('Linear ramsey fringes from PENTrack')
    plt.xlabel('W [Hz]')
    plt.ylabel('Sz')

    plt.savefig("ramseyFringe.png")
    print("ramseyFringe.png created")

    np.savetxt('ramseyAnalysis.out', (wVal,szAv), delimiter=",")
    print("ramseyAnalysis.out created")
    plt.show()
    return

if ( __name__ == '__main__' ):
    main()
