#!/usr/bin/env python
# Submits the jobs to make ramsey fringes to the torque queing system
# Uses file PBS_TEMPLATE as template for batch submission script
# Uses file CONFIG_TEMPLATE as the template for the ramsey cycle
# Assumes ramseyFringe.py is located in the /PENTrack directory

# Some initial parameters
W_STEP = 0.001    #[rad s^-1]    Step value of w to make ramsey fringes
W_VAL = 183.2   #[rad s^-1]    What w to start with
W_MAX  = 183.3    #[rad s^-1]    What w to end with
JOB_NUM_START = 0    # What job number at which to start labeling output files
PBS_TEMPLATE = 'ramseyPBS.txt'     # torque PBS script template file
CONFIG_TEMPLATE = 'ramseyConfig.txt'    # Ramsey pulse PENTrack config file
RAMSEY_STL ='in/ramseyChamber_d=1m_h=01m.stl'   # name of the ramsey chamber stl file

def main():
    import numpy as np
    from shutil import copyfile
    import os.path
    import datetime
    import subprocess

    if not os.path.isfile(RAMSEY_STL):
        print("Error: Cannot find " + RAMSEY_STL)
        return
    if not os.path.isfile(PBS_TEMPLATE):
        print("Error: Cannot find " + PBS_TEMPLATE)
        return
    if not os.path.isfile(CONFIG_TEMPLATE):
        print("Error: Cannot find " + CONFIG_TEMPLATE)
        return

    wRange = np.arange(W_VAL, W_MAX, W_STEP)
    jobCounter = JOB_NUM_START
    filenames = []

    if len(wRange)==0:
        print("Please adjust pulse frequency parameters in code")
        return

    print("Start pulse freq: ", wRange[0])
    print("Ending pulse freq: ", wRange[-1])
    print("Step size: ", W_STEP)
    print("Number of jobs: ", len(wRange))

    print("Submitting jobs")
    # Loop through pulse frequencies, copying the config file/job name with new parameters
    # Then submits the job
    for w in wRange:
        filenames.append(str(jobCounter).zfill(12) + "neutronend.out")
        configFileName = ('in/ramseyConfig' + str(jobCounter) + '.in')
        pbsFileName = ('ramsey' + str(jobCounter) + '.pbs')
        replacements = {'JOB_NUM':str(jobCounter), 'PULSE_FREQ':str(w), 'CONFIG_FILE':configFileName}
        jobCounter += 1
        with open(PBS_TEMPLATE) as infile, open(pbsFileName, 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():    #use iteritems() for python 2, items() for python 3
                    line = line.replace(src, target)
                outfile.write(line)
        with open(CONFIG_TEMPLATE) as infile, open(configFileName, 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():    #use iteritems() for python 2, items() for python 3
                    line = line.replace(src, target)
                outfile.write(line)
        # Submit job via bash
        process = subprocess.Popen(["qsub", pbsFileName])
        output, error =  process.communicate()
        # Remove generated file (NOTE: DO NOT DELETE CONFIG FILES UNTIL AFTER RUN!!!!!!)
        os.remove(pbsFileName)

    # Prints out file names with corresponding pulse frequency
    jobFile = open('out/joblist.out', "a")
    now = datetime.datetime.now()
    jobFile.write("# Jobs submitted " + now.strftime("%Y-%m-%d %H:%M") + "\n")
    for w, name in zip(wRange, filenames):
        jobFile.write(name + " "+ str(w) + "\n")
    jobFile.close()
    print("Job list + pi/2 pulse freqs written to PENTrack/out")


    return


if ( __name__ == '__main__' ):
    main()
