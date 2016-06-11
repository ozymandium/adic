#!/usr/bin/env python
"""

"""
# from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter, Timer
from ipdb import set_trace
import numpy as np
import cloudpickle
import sys, os
from tqdm import trange
from time import time
from util import shared_from_array

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
  m = np.unique(np.ceil(np.logspace(0, end_log_inc, n_pts))).astype(np.int64)
  T = m*t0

  theta_gyr = np.cumsum(gyr_arr, axis=1)
  theta_acc = np.cumsum(acc_arr, axis=1)

  sigma2_gyr = np.zeros((M, len(m)))
  sigma2_acc = np.zeros((M, len(m)))

  print 'Calculating'
  for ii in trange(len(m), desc='Loop over all Tau values', smoothing=True):
    i = int(ii)
    k = range(N - 2*m[i])
    sigma2_gyr[:,i] = np.sum( np.power( theta_gyr[:,k+2*m[i]] - 2*theta_gyr[:,k+m[i]] + theta_gyr[:,k] , 2 ), axis=1)
    sigma2_acc[:,i] = np.sum( np.power( theta_acc[:,k+2*m[i]] - 2*theta_acc[:,k+m[i]] + theta_acc[:,k] , 2 ), axis=1)

    # for kk in trange(1, int(N - 2*m[i]), desc='Loop within current Tau value'):
    #   k = int(kk)
    #   sigma2_gyr[:,i] += np.power( theta_gyr[:,k+2*m[i]] - 2*theta_gyr[:,k+m[i]] + theta_gyr[:,k] , 2 )
    #   sigma2_acc[:,i] += np.power( theta_acc[:,k+2*m[i]] - 2*theta_acc[:,k+m[i]] + theta_acc[:,k] , 2 )



  div = np.tile(2*np.multiply(np.power(T,2), N-2*m), (M,1))
  sigma2_gyr = np.divide(sigma2_gyr, div)
  sigma2_acc = np.divide(sigma2_acc, div)
  sigma_gyr = np.sqrt(sigma2_gyr)
  sigma_acc = np.sqrt(sigma2_acc)

  print 'saving'
  with open('/tmp/allan.cloudpickle', 'wb') as f:
    cloudpickle.dump(
      {
        'T': T,
        'sigma2_gyr': sigma2_gyr,
        'sigma2_acc': sigma2_acc,
        'sigma_gyr': sigma_gyr,
        'sigma_acc': sigma_acc,
      },
      f, -1
    )


if __name__ == '__main__':
  main()