from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter, Timer
import multiprocessing
import ctypes
import numpy as np
from scipy.signal import fftconvolve


def get_progress_bar(n):
  # progress bar
  pbar_widgets = ['IMU Epochs : ', Bar(marker='#'), 'epoch=', Counter(), ' ', Percentage(), ' (', Timer(), ') ', AdaptiveETA(), ' ']
  pbar = ProgressBar(widgets=pbar_widgets, maxval=n).start()
  return pbar


numpy_ctypes_map = {
  'float64': ctypes.c_double,
  'int64': ctypes.c_int64,
  'bool': ctypes.c_bool,
}


def shared_from_array(arr):
  # create shared memory object
  shared_arr_base = multiprocessing.Array(numpy_ctypes_map[str(arr.dtype)], arr.size)
  # create array representation
  shared_arr = np.ctypeslib.as_array(shared_arr_base.get_obj()).reshape(arr.shape)
  # copy data
  shared_arr[:] = arr[:]
  
  return shared_arr


def chunk(lst, n):
  """
  divide list `lst` into `n` unordered chunks
  http://stackoverflow.com/a/2136090
  """
  return [ lst[i::n] for i in xrange(n) ]


def autocorrelation(a):
  """use fft to compute the autocorrelation function of a timeseries signal
  """

  # # Stackoverflow
  # if len(a.shape) > 1:
  #   raise Exception('1D only!')
  # l = len(a)
  # b = np.zeros((l*2))
  # b[:l] = a
  # b = np.roll(b, l/4)
  # b.rotate(l/2)
  # return sp.fftconvolve(b, a[::-1, mode='valid')

  # # SciPy docs
  return fftconvolve(a, a[::-1], mode='full')


def scroll_avg_filter(y, N):
  """Wrapped averaging. only use this for data that should be static.
  It computes the rolling average of the ends of the data set using the opposite
  side of the timeseries
  this is efficient because it is insensitive to the size of the averaging window.
  """
  d = 2*N+1
  cs = np.cumsum(np.hstack((y[:,-N-1:], y, y[:,:N])), axis=1)
  return (cs[:,d:]-cs[:,:-d]) / np.float64(d)
