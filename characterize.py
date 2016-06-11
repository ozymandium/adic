#!/usr/bin/env python
import matplotlib.pyplot as plt
import cloudpickle
import sys, os


with open(os.path.abspath(sys.argv[1]), 'rb') as f:
  locals().update(cloudpickle.load(f))

plt.subplot(2,1,1)
plt.plot(T, sigma_gyr[0,:],
         T, sigma_gyr[1,:],
         T, sigma_gyr[2,:])
plt.xlabel('Tau')
plt.ylabel('\sigma Gyro')

plt.subplot(2,1,2)
plt.plot(T, sigma_acc[0,:],
         T, sigma_acc[1,:],
         T, sigma_acc[2,:])
plt.xlabel('Tau')
plt.ylabel('\sigma Accel')

plt.show()