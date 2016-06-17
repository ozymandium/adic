"""

"""
import numpy as np
import sys, os
import multiprocessing
from ipdb import set_trace
from util import *
import cloudpickle
from scipy.signal import filtfilt, butter
from time import time
from tqdm import trange




def main():

  data_dir, in_name = os.path.split(os.path.abspath(sys.argv[1]))
  set_name, ext = in_name.split('.')
  out_file_name = os.path.join(data_dir, set_name+'_acor.cloudpickle')
  print 'Data directory: ', data_dir
  print 'Data set name: ', set_name
  print 'Output autocorrelation file name:', out_file_name

  with open(os.path.join(data_dir, in_name), 'rb') as f:
    data = cloudpickle.load(f)
  print 'subtracting mean'
  time_arr = shared_from_array( data['time_arr'] - np.mean(data['time_arr']) )
  gyr_arr = shared_from_array( data['gyr_arr']   - np.tile( np.mean(data['gyr_arr'],  axis=1).reshape((3,1)), (1,data['gyr_arr'].shape[1]) ) )
  acc_arr = shared_from_array( data['acc_arr']   - np.tile( np.mean(data['acc_arr'],  axis=1).reshape((3,1)), (1,data['acc_arr'].shape[1]) ) )

  win_size_gyr = int(sys.argv[2])
  win_size_acc = int(sys.argv[3])
  print 'Averaging window size for gyro:  ', win_size_gyr
  print 'Averaging window size for accel: ', win_size_acc
  print 'filtering data'
  
  # # Wall recommends iterative zero-phase low pass filtering
  # b, a = butter(2, 0.1)
  # gyr_arr = filtfilt(b, a, gyr_arr, axis=1)
  # acc_arr = filtfilt(b, a, acc_arr, axis=1)
  
  # b_gyr = np.ones((win_size_gyr,))
  # b_acc = np.ones((win_size_acc,))
  # a_gyr = np.zeros((win_size_gyr+1,))
  # a_acc = np.zeros((win_size_acc+1,))
  # a_gyr[0] = np.float64(win_size_gyr)
  # a_acc[0] = np.float64(win_size_acc)

  # gyr_arr = filtfilt(b_gyr, a_gyr, gyr_arr, axis=1)
  # acc_arr = filtfilt(b_acc, a_acc, acc_arr, axis=1)

  # rather than try to design a filter iteratively by selecting cutoff frequencies
  # simply do windowed averaging
  gyr_arr = scroll_avg_filter(gyr_arr, win_size_gyr)
  acc_arr = scroll_avg_filter(acc_arr, win_size_acc)


  N = len(time_arr)

  acor_gyr = np.empty((3,2*N-1))
  acor_acc = np.empty((3,2*N-1))

  print 'calculating autocorrelation...'
  for i in range(3):
    acor_gyr[i,:] = autocorrelation(gyr_arr[i,:])
    acor_acc[i,:] = autocorrelation(acc_arr[i,:])
  print 'done. saving data...'

  with open(out_file_name, 'wb') as f:
    cloudpickle.dump(
      {
        'win_size_gyr': win_size_gyr,
        'win_size_acc': win_size_acc,
        'gyr_arr_filt': gyr_arr,
        'acc_arr_filt': acc_arr,
        'acor_gyr': acor_gyr[:,N:],
        'acor_acc': acor_acc[:,N:],
      },
      f, -1
    )