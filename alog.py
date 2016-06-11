import sys, os
from sensors import IMUEpoch
import numpy as np
from main import get_progress_bar


DATA_TYPE = np.float32


def file_line_count(file_name):
  with open(file_name, 'r') as f:
    for i, l in enumerate(f):
      pass
  return i+1


def find_alog_file(folder):
  # everyting that might be an alog file
  alog_files = [f for f in os.listdir(folder) if '.alog' in f]
  if len(alog_files) > 1:
    # could have *.alog.bak or something. get rid of that
    alog_files = [f for f in alog_files if f[-5:] == '.alog']
    # don't want to 
    if len(alog_files) > 1:
      return None
  elif len(alog_files) == 0:
    return None
  return os.path.join(folder, alog_files[0])


def string_to_float_vector(s):
  return [DATA_TYPE(v) for v in s.split('{')[1].rstrip('}').split(',')]


def parse_imu_separate(alog_filen, app_name, gyr_names, acc_names):
  """
  parse IMU data where each measurement is 

  :param dict data_sensor: data[sensor] from above
  :return liat:
  """
  print 'Counting lines in alog file.'
  n_lines = file_line_count(alog_filen)

  print 'Preallocating'
  # allocate more than will be needed
  n_gyr_names = len(gyr_names)
  n_acc_names = len(acc_names)
  time_arr = np.empty((n_lines))
  gyr_arr = np.empty((n_gyr_names, n_lines))
  acc_arr = np.empty((n_acc_names, n_lines))

  line_count = 0
  data_count = 0
  pbar = get_progress_bar(n_lines)

  var_names = list(gyr_names) + list(acc_names)
  cur_time = {n: None for n in var_names}
  cur_data = {n: None for n in var_names}

  print 'Iterating through file'
  with open(alog_filen, 'r') as alog_file:
    for line in alog_file:
      if line[0] == '%':
        line_count += 1
        pbar.update(line_count)
        continue
      fields = line.split()
      sensor = fields[2]
      if sensor != app_name:
        line_count += 1
        pbar.update(line_count)
        continue
      name = fields[1]
      if name not in var_names:
        line_count += 1
        pbar.update(line_count)
        continue
      cur_time[name] = DATA_TYPE(fields[0])
      cur_data[name] = DATA_TYPE(fields[3])

      # check to see if epoch is complete
      if len(set(cur_time.values())) == 1:
        time_arr[data_count] = cur_time[gyr_names[0]]
        gyr_arr[:,data_count] = [cur_data[req_name] for req_name in gyr_names]
        acc_arr[:,data_count] = [cur_data[req_name] for req_name in acc_names]
        data_count += 1

      line_count += 1
      pbar.update(line_count)

  # chop off end of arrays that didn't get filled
  print 'resizing'
  gyr_arr = np.resize(gyr_arr, (n_gyr_names, data_count))
  acc_arr = np.resize(acc_arr, (n_acc_names, data_count))

  # Every time you rewrite a parser function to get data into arrays,
  # it needs to output a dict with these fields and data types, even if one of 
  # the array fields has an empty matrix
  return {
    'source_file_name': alog_filen,
    'time_arr': time_arr,
    'gyr_arr': gyr_arr,
    'acc_arr': acc_arr,
  }
