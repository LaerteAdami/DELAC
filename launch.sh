#!/bin/bash
#SBATCH --mail-user=laerte.adami@city.ac.uk       # useful to get an email when jobs starts
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH -D /users/adcy359/DELAC    # Working directory
#SBATCH --job-name test                      # Job name
#SBATCH --partition=gengpu                         # Select the correct partition.
#SBATCH --nodes=1                                  # Run on 1 nodes (each node has 48 cores)
#SBATCH --ntasks-per-node=1                        # Run one task
#SBATCH --cpus-per-task=4                          # Use 4 cores, most of the procesing happens on the GPU
#SBATCH --mem=12GB                                 # Expected ammount CPU RAM needed (Not GPU Memory)
#SBATCH --time=02:00:00                            # Expected ammount of time to run Time limit hrs:min:sec
#SBATCH --gres=gpu:1                               # Use one gpu.
#SBATCH -e Results/%x_%j.e                         # Standard output and error log [%j is replaced with the jobid]
#SBATCH -o Results/%x_%j.o                         # [%x with the job name], make sure 'results' folder exists.

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

#Remove any unwanted modules
module purge

#Modules required
module load python/3.7.12
/opt/apps/python/3.7.12/bin/python3 -m pip install --upgrade --proxy http://hpc-proxy00.city.ac.uk:3128 --user pip
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user fenics-dolfin
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user gymnasium
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user numpy
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user matplotlib
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user 'stable-baselines3[extra]'
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user gmsh
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user pybind11==2.2.4
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user turtleFSI
pip install --proxy http://hpc-proxy00.city.ac.uk:3128 --user --no-index -r Requirements.txt

#Run your script
python3 -u main.py