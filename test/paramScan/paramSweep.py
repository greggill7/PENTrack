#!/usr/bin/env python
from __future__ import print_function
import numpy as np
from shutil import copyfile
from distutils.util import strtobool
import os.path
import datetime
import subprocess

# Variables that will be altered in PBS_TEMPLATE
# to generate temp job files: JOB_START JOB_END CONFIG_FILE
#
# Variables that will be altered in CONFIG_TEMPLATE
# to generate temp config files: PARAM
#
# Now input values of your choice here:
D_STEP_NUM = 20  #Number of steps in your scan
D_START = 0.01   #What PARAM to start with
D_END  = 1    #What PARAM to end with
D_ROUND = 3     #Decimal places to round scan steps to
JOB_NUM_START = 0    # What job number at which to start labeling output files
JOBS_PER_STEP = 10      # Number of jobs per step
PBS_TEMPLATE = 'in/jobParamScan.pbs'     # torque PBS script template file
CONFIG_TEMPLATE = 'in/configRamp.in'    # PENTrack config file

def main():
    # Error handling
    if not os.path.isfile(PBS_TEMPLATE):
        print("Error: Cannot find " + PBS_TEMPLATE)
        return
    if not os.path.isfile(CONFIG_TEMPLATE):
        print("Error: Cannot find " + CONFIG_TEMPLATE)
        return

    dRange = np.linspace(D_START, D_END, D_STEP_NUM,endpoint=True).round(D_ROUND)
    jobCounter = JOB_NUM_START
    filenames = []

    if len(dRange)==0:
        print("Please adjust parameters in code")
        return

    print("Start param: ", dRange[0])
    print("End param: ", dRange[-1])
    print("Sweep steps:", D_STEP_NUM)
    print('Start job num: ', JOB_NUM_START)
    print("Total jobs: ", len(dRange)*JOBS_PER_STEP)
    if not strtobool(raw_input("Continue? (y/n): ")):
        return

    if(len(dRange)*JOBS_PER_STEP > 400):
        print("Error: Total job number larger than acceptable in Torque queue")
        print("Exiting")
        return

    print("Submitting jobs")
    # Loop through pulse frequencies, copying the config file/job name with new parameters
    # Then submits the job
    for d in dRange:
        jobEnd = jobCounter + JOBS_PER_STEP - 1
        filenames.append(str(jobCounter) + "\t" + str(jobEnd))
        configFileName = ('./in/tempConfig' + str(jobCounter) + '.in')
        pbsFileName = ('temp' + str(jobCounter) + '.pbs')
        replacements = {'JOB_START':str(jobCounter), 'JOB_END':str(jobEnd), 'PARAM':str(d), 'CONFIG_FILE':configFileName}
        jobCounter += JOBS_PER_STEP
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
    jobFile.write("# start\tend\tparam\n")
    for d, name in zip(dRange, filenames):
        jobFile.write(name + "\t"+ str(d) + "\n")
    jobFile.close()
    print("Job list written to PENTrack/out")


    return


if ( __name__ == '__main__' ):
    main()
