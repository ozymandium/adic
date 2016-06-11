#!/usr/bin/env python
"""

"""
# from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter, Timer
from ipdb import set_trace
import numpy as np
import cloudpickle
import sys, os
from tqdm import trange, tqdm
from time import time
from util import shared_from_array, get_progress_bar
import multiprocessing
import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument('in_file', help='large input text file (newline delimited)')
argparser.add_argument('out_file', help='output file')
argparser.add_argument('-p', '--points', default=10000)



def adev_at_tau(sigma2, theta, m, N, ii):
  """worker function for parallelization. first part of the Allan deviation 
  equation
  """
  i = int(ii)
  k = range(N - 2*m[i])
  sigma2[:,i] = np.sum( np.power( theta[:,k+2*m[i]] - 2*theta[:,k+m[i]] + theta[:,k] , 2 ), axis=1)


def main():

  args = argparser.parse_args()
  n_pts = int(args.points)

  print 'Loading data'
  with open(os.path.abspath(args.in_file), 'rb') as f:
    data = cloudpickle.load(f)
  time_arr = data['time_arr']
  gyr_arr = data['gyr_arr']
  acc_arr = data['acc_arr']
  
  # M: number of axes
  # N: number of epochs
  if acc_arr.shape != gyr_arr.shape:
    raise Exception('different sizes')
  M, N = gyr_arr.shape

  # automate this?
  print 'Computing mean dt'
  fs = np.mean(np.diff(time_arr))
  t0 = np.float64(1.0)/fs

  n = np.power(2, np.arange(np.floor(np.log2(N/2.))))
  end_log_inc = np.log10(n[-1])
  m = shared_from_array( np.unique(np.ceil(np.logspace(0, end_log_inc, n_pts))).astype(np.int64) )
  T = m*t0

  # setup input/output shared memory arrays
  theta_gyr = shared_from_array( np.cumsum(gyr_arr, axis=1) )
  theta_acc = shared_from_array( np.cumsum(acc_arr, axis=1) )
  sigma2_gyr = shared_from_array( np.zeros((M, len(m))) )
  sigma2_acc = shared_from_array( np.zeros((M, len(m))) )

  print 'creating procs'
  gyr_procs = [multiprocessing.Process(target=adev_at_tau, args=(sigma2_gyr, theta_gyr, m, N, i)) for i in xrange(len(m))]
  acc_procs = [multiprocessing.Process(target=adev_at_tau, args=(sigma2_acc, theta_acc, m, N, i)) for i in xrange(len(m))]
  for i in trange(len(m), desc='starting procs'):
    gyr_procs[i].start()
    acc_procs[i].start()
  print 'joining procs'
  for i in range(len(m)):
    gyr_procs[i].join()
    acc_procs[i].join()

  print 'full batch operations'

  div = np.tile(2*np.multiply(np.power(T,2), N-2*m), (M,1))
  sigma2_gyr = np.divide(sigma2_gyr, div)
  sigma2_acc = np.divide(sigma2_acc, div)
  sigma_gyr = np.sqrt(sigma2_gyr)
  sigma_acc = np.sqrt(sigma2_acc)

  out_file_name = os.path.abspath(args.out_file)
  print 'saving to: ', out_file_name
  with open(out_file_name, 'wb') as f:
    cloudpickle.dump(
      {
        'T': np.array(T),
        'sigma2_gyr': sigma2_gyr,
        'sigma2_acc': sigma2_acc,
        'sigma_gyr': sigma_gyr,
        'sigma_acc': sigma_acc,
      },
      f, -1
    )