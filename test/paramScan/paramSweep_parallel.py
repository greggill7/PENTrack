#!/usr/bin/env python
# Now utilizes GNU Parallel to run multiple PENTrack simulations per job
from __future__ import print_function
import numpy as np
from shutil import copyfile
from distutils.util import strtobool
import os.path
import datetime
import subprocess
import argparse

# Variables that will be altered in PBS_TEMPLATE
# to generate temp job files: JOB_START JOB_END CONFIG_FILE
#
# Variables that will be altered in CONFIG_TEMPLATE
# to generate temp config files: PARAM
#
# Now input values of your choice here:
D_STEP_NUM = 2  #Number of steps in your scan
D_START = 0   #What PARAM to start with
D_END  = 1    #What PARAM to end with
D_ROUND = 3     #Decimal places to round scan steps to
JOB_NUM_START = 3000    # What job number at which to start labeling output files
JOBS_PER_STEP = 10      # Number of jobs per scan step
PARALLEL_PER_JOB = 10   # Number of PENTrack instances per job
PBS_TEMPLATE = 'in/jobParamScan_parallel.pbs'     # torque PBS script template file
CONFIG_TEMPLATE = 'in/configRamp.in'    # PENTrack config file
OUTPUT_DIRECTORY = '/N/dc2/scratch/dkwong/' # Where to output PENTrack files

dRange = np.linspace(D_START, D_END, D_STEP_NUM,endpoint=True).round(D_ROUND)

def main():
    parser = argparse.ArgumentParser(description='Utilizes GNU Parallel to run multiple PENTrack simulations per job')
    parser.add_argument('-s', '--submit', action='store_true', help = 'Submits job to queue')
    parser.add_argument('-r', '--run', action='store_true', help = 'Called when run by cluster')
    parser.add_argument('-js', '--jobStart', type=int, help = 'Called when run by cluster')
    parser.add_argument('-je', '--jobEnd', type=int, help = 'Called when run by cluster')
    parser.add_argument('-c', '--configFile', type=str, help = 'Called when run by cluster')

    args = parser.parse_args()

    # Submit jobs to queue
    if args.submit:
        # Error handling
        if not os.path.isfile(PBS_TEMPLATE):
            print('Error: Cannot find ' + PBS_TEMPLATE)
            return
        if not os.path.isfile(CONFIG_TEMPLATE):
            print('Error: Cannot find ' + CONFIG_TEMPLATE)
            return

        jobCounter = JOB_NUM_START
        runNames = []

        if len(dRange)==0:
            print('Invalid parameter sweep range. Edit in code')
            return

        printParameters()
        if not strtobool(raw_input('\nContinue? (y/n): ')):
            return

        if(len(dRange)*JOBS_PER_STEP > 400):
            print('Error: Total job number larger than acceptable in Carbonate Torque queue')
            print('Exiting')
            return

        print('Submitting jobs')
        # Loop through pulse frequencies, copying the config file/job name with new parameters
        # Then submits the job
        for d in dRange:
            # For joblist.out
            jobEnd = jobCounter + JOBS_PER_STEP*PARALLEL_PER_JOB - 1
            runNames.append(str(jobCounter) + '\t' + str(jobEnd))

            # Create config file
            configFileName = ('./in/tempConfig' + str(jobCounter) + '.in')
            replacements = {'PARAM':str(d)}
            copyAndReplace(CONFIG_TEMPLATE, configFileName, replacements)

            # Create pbs submission file for each job
            for j in np.arange(JOBS_PER_STEP):
                start = jobCounter + j*PARALLEL_PER_JOB
                end = jobCounter + (j+1)*PARALLEL_PER_JOB -1

                replacements = {'JOB_START':str(start), 'JOB_END':str(end), 'PARAM':str(d), 'CONFIG_FILE':configFileName}
                pbsFileName = ('temp' + str(jobCounter) + '.pbs')
                copyAndReplace(PBS_TEMPLATE, pbsFileName, replacements)

                # Submit job via bash
                process = subprocess.Popen(['qsub', pbsFileName])
                output, error =  process.communicate()
                # Remove generated pbs file (NOTE: DO NOT DELETE CONFIG FILES UNTIL AFTER RUN!!!!!!)
                os.remove(pbsFileName)

            # Update job counter and loop back
            jobCounter += JOBS_PER_STEP*PARALLEL_PER_JOB

        # Prints out file names with corresponding pulse frequency
        jobFile = open('out/joblist.out', 'a')
        now = datetime.datetime.now()
        jobFile.write('# Jobs submitted ' + now.strftime('%Y-%m-%d %H:%M') + '\n')
        jobFile.write('# start\tend\tparam\n')
        for d, name in zip(dRange, runNames):
            jobFile.write(name + '\t'+ str(d) + '\n')
        jobFile.close()
        print('Job list written to PENTrack/out')
        return

    # For when the cluster runs the job
    if args.run:
        if None in (args.jobStart, args.jobEnd, args.configFile):
            print('Missing dependent flag when calling [--run], see [--help]')
            return
        print('Creating GNU Parallel Runfile...', end='')
        runfileName = 'in/runfile' + str(args.jobStart) + '-' + str(args.jobEnd) + '.in'
        with open(runfileName, 'w') as runfile:
            for jobnum in np.arange(args.jobStart, args.jobEnd + 1):
                runfile.write('./PENTrack ' + str(jobnum) +' ' + args.configFile + ' ' + OUTPUT_DIRECTORY \
                              + ' >> ' + noExt(OUTPUT_DIRECTORY, '/') + '/output.txt-' + str(jobnum) +'\n')
        print('Done\nLaunching parallel instances for jobs ' + str(args.jobStart) + ' - ' + str(args.jobEnd))
        process = subprocess.Popen(['parallel < ' + str(runfileName)], shell=True)
        output, error =  process.communicate()

        print('Removing runfile')
        os.remove(runfileName)
        return

    print('To submit to queue: paramSweep_parallel --submit')
    print('\nParameters (Change in code)')
    printParameters()

    return

# Removes the extension name from a filename if present
def noExt(filename, extensionName):
    if filename[-len(extensionName):].find(extensionName) != -1:
        return filename[:-len(extensionName)]
    return filename

def copyAndReplace(IN_NAME, OUT_NAME, replacements):
    with open(IN_NAME) as infile, open(OUT_NAME, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():    #use iteritems() for python 2, items() for python 3
                line = line.replace(src, target)
            outfile.write(line)
    return

def printParameters():
    print('Start param: ', D_START)
    print('End param: ', D_END)
    print('Num. sweep steps:', D_STEP_NUM)
    print('Start job num: ', JOB_NUM_START)
    print('Jobs per step: ', JOBS_PER_STEP)
    print('Total jobs: ', len(dRange)*JOBS_PER_STEP)
    print('Parallel PENTrack instances per job: ', PARALLEL_PER_JOB)
    print('Total output files', len(dRange)*JOBS_PER_STEP*PARALLEL_PER_JOB)
    print('PBS Template: ', PBS_TEMPLATE)
    print('Config Template: ', CONFIG_TEMPLATE)
    print('Output directory: ', OUTPUT_DIRECTORY)
    return


if ( __name__ == '__main__' ):
    main()
