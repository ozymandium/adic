#!/usr/bin/env python
import matplotlib.pyplot as plt
import cloudpickle
import sys, os
from ipdb import set_trace


def main():

  with open(os.path.abspath(sys.argv[1]), 'rb') as f:
    data = cloudpickle.load(f)

  T = data['T']
  sigma_gyr = data['sigma_gyr']
  sigma_acc = data['sigma_acc']

  plt.subplot(2,1,1)
  plt.loglog(T, sigma_gyr[0,:],
             T, sigma_gyr[1,:],
             T, sigma_gyr[2,:])
  plt.xlabel('Tau')
  plt.ylabel('\sigma Gyro')

  plt.subplot(2,1,2)
  plt.loglog(T, sigma_acc[0,:],
             T, sigma_acc[1,:],
             T, sigma_acc[2,:])
  plt.xlabel('Tau')
  plt.ylabel('\sigma Accel')

  plt.show()