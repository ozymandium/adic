from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter, Timer
import multiprocessing
import ctypes
import numpy as np

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