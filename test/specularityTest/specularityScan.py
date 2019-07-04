#!/usr/bin/env python
from __future__ import print_function
import numpy as np
from shutil import copyfile
import os.path
import datetime
import subprocess

# Some initial parameters
D_STEP_NUM = 2  #Number of steps in your scan
D_START = 0   #What specularity to start with
D_END  = 0.05    #What specularity to end with
JOB_NUM_START = 0    # What job number at which to start labeling output files
JOB_PARALLEL = 200      # Number of parallel jobs per step
PBS_TEMPLATE = 'in/jobSpec_parallel.pbs'     # torque PBS script template file
CONFIG_TEMPLATE = 'in/configT2.in'    # Ramsey pulse PENTrack config file

def main():
    if not os.path.isfile(PBS_TEMPLATE):
        print("Error: Cannot find " + PBS_TEMPLATE)
        return
    if not os.path.isfile(CONFIG_TEMPLATE):
        print("Error: Cannot find " + CONFIG_TEMPLATE)
        return

    dRange = np.linspace(D_START, D_END, D_STEP_NUM,endpoint=True)
    jobCounter = JOB_NUM_START
    filenames = []

    if len(dRange)==0:
        print("Please adjust parameters in code")
        return

    print("Start specularity: ", dRange[0])
    print("Ending specularity: ", dRange[-1])
    print("Number of steps:", D_STEP_NUM)
    print("Number of jobs: ", len(dRange)*JOB_PARALLEL)

    if(len(dRange)*JOB_PARALLEL > 400):
        print("Error: Total job number larger than acceptable in Torque queue")
        print("Exiting")
        return

    print("Submitting jobs")
    # Loop through pulse frequencies, copying the config file/job name with new parameters
    # Then submits the job
    for d in dRange:
        jobEnd = jobCounter + JOB_PARALLEL - 1
        filenames.append(str(jobCounter) + "\t" + str(jobEnd))
        configFileName = ('./in/tempConfig' + str(jobCounter) + '.in')
        pbsFileName = ('temp' + str(jobCounter) + '.pbs')
        replacements = {'JOB_START':str(jobCounter), 'JOB_END':str(jobEnd), 'SPEC':str(d), 'CONFIG_FILE':configFileName}
        jobCounter += JOB_PARALLEL
        with open(PBS_TEMPLATE) as infile, open(pbsFileName, 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():    #use iteritems() for python 2, items() for python 3
                    line = line.replace(src, target)
                outfile.write(line)
        with open(CONFIG_TEMPLATE) as infile, open(configFileName, 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():    #use iteritems() for python 2, items() for python 3
                    line = line.replace(src, target)
                outfile.write(line)
        # Submit job via bash
        process = subprocess.Popen(["qsub", pbsFileName])
        output, error =  process.communicate()
        # Remove generated pbs file (NOTE: DO NOT DELETE CONFIG FILES UNTIL AFTER RUN!!!!!!)
        os.remove(pbsFileName)

    # Prints out file names with corresponding pulse frequency
    jobFile = open('out/joblist.out', "a")
    now = datetime.datetime.now()
    jobFile.write("# Jobs submitted " + now.strftime("%Y-%m-%d %H:%M") + "\n")
    jobFile.write("# start\tend\tspecularity\n")
    for d, name in zip(dRange, filenames):
        jobFile.write(name + "\t"+ str(d) + "\n")
    jobFile.close()
    print("Job list written to PENTrack/out")


    return


if ( __name__ == '__main__' ):
    main()
