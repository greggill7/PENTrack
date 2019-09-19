paramScan
==========
In this folder I have included some scripts that allow parameter sweeps  
This assumes you're submitting jobs on a TORQUE queuing system  
When using these scripts, paramSweep.py should be located in /PENTrack,  
and I would recommend putting your CONFIG_TEMPLATE and PBS_TEMPLATE in /PENTrack/in

paramSweep.py
--------------
This is the parameter-scanning script that automatically generates config files and submits correctly numbered jobs.  
It takes a template config file  (CONFIG_TEMPLATE) and a template pbs submission file (PBS_TEMPLATE)  
Within these files, the PARAM keyword will be automatically replaced by the parameter you would like  
to sweep across  

The job numbering, and number of parallel jobs can be edited by JOB_NUM_START  
and JOBS_PER_STEP. Edit settings in the body of the code.  

Output: joblist.out -- Contains job numbers and the parameter used in those jobs


jobParamScan.pbs
-----------------
This is the PBS_TEMPLATE I would recommend using. You will obviously have to change your email address and folder directories  

Example sweeps
--------------

### PPM
This examines neutron transmission as the strength of a Pre-polarizing magnet is increased.  

ppmAnalysis.py -- Reads from joblist.out to make histograms and plots on neutron energy spectrum and flux  

### RamseyFringe
This generates rabi and ramsey fringes by sweeping across RF pulse frequencies  

ramseyAnalysis.py -- Reads from joblist.out to plot the ramsey/rabi fringe  

### specularityTest
This examines T2 times in a holding cell with large gradients in B. Sweeps across cell specularity  

specAnalysis.py -- Reads from joblist.out to calculate T2 and make plots. This takes quite a while to run
specAnalysis.pbs -- Job submission file since specAnalysis takes a long while to process all spin tracking files  
