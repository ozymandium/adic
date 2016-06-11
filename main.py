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


# def crunch_(sigma2, theta, m, ii):
#   i = int(ii)
#   k = range(N - 2*m[i])
#   sigma2[:,i] = np.sum( np.power( theta[:,k+2*m[i]] - 2*theta[:,k+m[i]] + theta[:,k] , 2 ), axis=1)


def crunch_(*args):
  sigma2 = args[0]
  theta = args[1]
  m = args[2]
  i = int(args[3])
  k = range(N - 2*m[i])
  sigma2[:,i] = np.sum( np.power( theta[:,k+2*m[i]] - 2*theta[:,k+m[i]] + theta[:,k] , 2 ), axis=1)


def genit(sigma2, theta, m, desc):
  for i in range(len(m)):
    yield sigma2, theta, m, i


# def genit(sigma2, theta, m, range_it):
#   yield ((sigma2, theta, m, ii) for ii in range_it)


def main():

  print 'Loading data'
  with open(os.path.abspath(sys.argv[1]), 'rb') as alog_file:
    data = cloudpickle.load(alog_file)
  gyr_arr = data['gyr_arr']
  acc_arr = data['acc_arr']
  
  # M: number of axes
  # N: number of epochs
  if acc_arr.shape != gyr_arr.shape:
    raise Exception('different sizes')
  M, N = gyr_arr.shape

  # automate this?
  fs = np.float64(100)
  t0 = np.float64(1.0)/fs

  n_pts = 10000

  n = np.power(2, np.arange(np.floor(np.log2(N/2.))))
  end_log_inc = np.log10(n[-1])
  m = shared_from_array( np.unique(np.ceil(np.logspace(0, end_log_inc, n_pts))).astype(np.int64) )
  T = m*t0

  # setup input/output shared memory arrays
  theta_gyr = shared_from_array( np.cumsum(gyr_arr, axis=1) )
  theta_acc = shared_from_array( np.cumsum(acc_arr, axis=1) )
  sigma2_gyr = shared_from_array( np.zeros((M, len(m))) )
  sigma2_acc = shared_from_array( np.zeros((M, len(m))) )

  # for ii in trange(len(m), desc='Loop over all Tau values', smoothing=True):
  pool = multiprocessing.Pool(4)
  tic_prime = time()

  # loop over gyro
  print 'Calculating gyro allan dev'
  # tic_gyr = time()
  gyr_arg_it = genit(sigma2_gyr, theta_gyr, m, 'Gyro')
  res_gyr = pool.map(crunch_, gyr_arg_it)
  # print 'Gyro time: ', time() - tic_gyr
  
  # loop over accel
  print 'Calculating accel allan dev'
  # tic_acc = time()
  acc_arg_it = genit(sigma2_acc, theta_acc, m, 'Accel')
  res_acc = pool.map(crunch_, acc_arg_it)
  # print 'Accel time: ', time() - tic_acc

  pool.close()
  print 'Total time: ', time() - tic_prime, 's'

  div = np.tile(2*np.multiply(np.power(T,2), N-2*m), (M,1))
  sigma2_gyr = np.divide(sigma2_gyr, div)
  sigma2_acc = np.divide(sigma2_acc, div)
  sigma_gyr = np.sqrt(sigma2_gyr)
  sigma_acc = np.sqrt(sigma2_acc)

  out_file_name = os.path.abspath(sys.argv[2])
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


if __name__ == '__main__':
  main()