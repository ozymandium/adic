#!/usr/bin/env python
"""
Example of how to parse MOOS alog data into the NumPy arrays expected by this
package. Saves a data file.

Usage:
  
  ./example_moos_xbow440.py <recorded_data>.alog <out_file>.cloudpickle
"""
import sys, os
from alog import parse_imu_separate
import cloudpickle
import numpy as np

# first command line argument is the path to the alog file
source_file_name = os.path.abspath(sys.argv[1])
# data_dir = 

# get the data out of the alog file into 3 x n arrays (one each for gyro, accel)
data = parse_imu_separate(
  source_file_name,
  'gXbow440', 
  ('zGyroX_gXbow440', 'zGyroY_gXbow440', 'zGyroZ_gXbow440'),
  ('zAccelX_gXbow440', 'zAccelY_gXbow440', 'zAccelZ_gXbow440')
)

# optionally save the parsed matrices
# out_file_name = '/tmp/xbow440_parsed_arrays.cloudpickle'
out_file_name = os.path.abspath(sys.argv[2])
print 'Saving arrays to disc: ', out_file_name
with open(out_file_name, 'wb') as f:
  cloudpickle.dump(data, f, -1)