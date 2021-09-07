#!/bin/bash
#SBATCH -N 1
#SBATCH -t 10-0
#SBATCH -o /p/lustre2/sema1/fitsnap_test/HfO2/%j.job
#SBATCH -e /p/lustre2/sema1/fitsnap_test/HfO2/%j.err
#SBATCH -J FitSNAP
#SBATCH -p pdebug
#SBATCH --tasks-per-node=36
#SBATCH --qos=exempt
##SBATCH --exclusive=user

# loads Open MPI and libraries
module load mkl/2020.0
module load openmpi/4.1.0
module load intel/2021.3

# For the Intel MPI environent
source /usr/tce/packages/oneapi/oneapi-2021.3/setvars.sh
export I_MPI_FABRICS=shm:ofi

#ulimit -s unlimited

eval "$(/usr/workspace/wsa/sema1/anaconda3/bin/conda shell.bash hook)"
conda activate nff

export LAMMPSDIR=/usr/WS1/sema1/lammps
export FITSNAPDIR=/usr/WS1/sema1/FitSNAP

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$LAMMPSDIR/src
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:$LAMMPSDIR/src

export PYTHONPATH=${PYTHONPATH}:$LAMMPSDIR/python
export PYTHONPATH=${PYTHONPATH}:$FITSNAPDIR/python

ln -s $FITSNAPDIR/fitsnap3 .
ln -s $LAMMPSDIR/src/liblammps.so .
ln -s $LAMMPSDIR/python/lammps.py .

srun -n36 python -m fitsnap3 HfO2-example.in
