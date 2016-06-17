#!/usr/bin/env python
import numpy as np
from time import time
import matplotlib.pyplot as plt
from scipy.signal import filtfilt

def cwmean1(arr, n):
  warr = arr.copy()
  for i in range(n):
    warr += np.roll(arr, i+1)
    warr += np.roll(arr, -i-1)
  warr /= np.float64(2*n+1)
  return warr


def cwmean2(y, N):
  d = 2*N+1
  cs = np.cumsum(np.hstack((y[:,-N-1:], y, y[:,:N])), axis=1)
  return (cs[:,d:]-cs[:,:-d]) / np.float64(d)


y = np.random.random((2,10000))
# y = np.array(
#   [
#     [0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0,],
#     # np.arange(5),
#     # np.arange(5),
#   ],
#   dtype=np.float64,
# )
x = np.arange(y.shape[1])
N = 100

tic = time()
y1 = cwmean1(y, N)
print 'time for 1: ', time() - tic

tic = time()
d = 2*N+1
cs = np.cumsum(np.hstack((y[:,-N-1:], y, y[:,:N])), axis=1)
y2 = (cs[:,d:]-cs[:,:-d]) / (np.float64(d))
print 'time for 2: ', time() - tic
assert y2.shape == y.shape
print 'correct: ', np.allclose(y1, y2)


plt.figure()
plt.title('orig')
plt.plot(x, y[0,:], x, y[1,:])

plt.figure()
plt.title('1')
plt.plot(x, y1[0,:], x, y1[1,:])

plt.figure()
plt.title('2')
plt.plot(x, y2[0,:], x, y2[1,:])

plt.show()