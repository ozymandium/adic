"""

"""
import numpy as np
import sys, os
import multiprocessing
from ipdb import set_trace
from util import shared_from_array, autocorrelation
import cloudpickle
from scipy import signal


def avg_filter(arr, n):
  warr = arr.copy()
  for i in range(n):
    warr += np.roll(arr, i+1)
    warr += np.roll(arr, -i-1)
  warr /= np.float64(2*n+1)
  return warr


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
  time_arr = data['time_arr'] - np.mean(data['time_arr'])
  gyr_arr = data['gyr_arr']   - np.tile( np.mean(data['gyr_arr'],  axis=1).reshape((3,1)), (1,data['gyr_arr'].shape[1]) )
  acc_arr = data['acc_arr']   - np.tile( np.mean(data['acc_arr'],  axis=1).reshape((3,1)), (1,data['acc_arr'].shape[1]) )

  print 'filtering data'

  # # Wall recommends iterative zero-phase low pass filtering
  # b, a = signal.butter(2, 0.1)
  # gyr_arr = signal.filtfilt(b, a, gyr_arr, axis=1)
  # acc_arr = signal.filtfilt(b, a, acc_arr, axis=1)

  # rather than try to design a filter iteratively by selecting cutoff frequencies
  # simply do windowed averaging
  gyr_arr = avg_filter(gyr_arr, int(sys.argv[2]))
  acc_arr = avg_filter(acc_arr, int(sys.argv[2]))

  print 'done'


  N = len(time_arr)

  acor_gyr = np.empty((3,2*N-1))
  acor_acc = np.empty((3,2*N-1))

  print 'calculating...'
  for i in range(3):
    acor_gyr[i,:] = autocorrelation(gyr_arr[i,:])
    acor_acc[i,:] = autocorrelation(acc_arr[i,:])
  print 'done'

  with open(out_file_name, 'wb') as f:
    cloudpickle.dump(
      {
        'acor_gyr': acor_gyr[:,N-1:],
        'acor_acc': acor_acc[:,N-1:],
      },
      f, -1
    )