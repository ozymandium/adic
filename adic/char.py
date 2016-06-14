"""

"""
import pyqtgraph as pg
import cloudpickle
import sys, os
from ipdb import set_trace
import numpy as np
from scipy.interpolate import interp1d
import signal


blue = pg.mkPen(color='b')
green = pg.mkPen(color='g')
red = pg.mkPen(color='r')


def sigint_handler(*args):
  pg.QtGui.QApplication.quit()


def main():

  data_dir, in_name = os.path.split(os.path.abspath(sys.argv[1]))
  set_name, ext = in_name.split('.')
  adev_file_name = os.path.join(data_dir, set_name+'_adev.cloudpickle')
  acor_file_name = os.path.join(data_dir, set_name+'_acor.cloudpickle')
  print 'Data directory: ', data_dir
  print 'Data set name: ', set_name
  print 'Allan deviation file:', adev_file_name
  print 'Autocorrelation file:', acor_file_name

  print 'Loading data files...'
  with open(os.path.abspath(sys.argv[1]), 'rb') as f:
    data = cloudpickle.load(f)
  with open(adev_file_name, 'rb') as f:
    adev = cloudpickle.load(f)
  with open(acor_file_name, 'rb') as f:
    acor = cloudpickle.load(f)

  t0 = np.mean(np.diff(data['time_arr']))
  fs = np.float64(1.0)/t0

  T = adev['T']
  sigma_gyr = adev['sigma_gyr']
  sigma_acc = adev['sigma_acc']
  sigma2_gyr = adev['sigma2_gyr']
  sigma2_acc = adev['sigma2_acc']

  acor_gyr = acor['acor_gyr']
  acor_acc = acor['acor_acc']
  acor_dt = np.arange(acor_gyr.shape[1])*t0

  #### compute measurement noise (random walk statistics)

  print 'Measurement Noise:'

  print '  Gyro'
  sigma2_gyr_lspl = interp1d(T, sigma2_gyr, axis=1, copy=False)
  sigma2_gyr_T1 = sigma2_gyr_lspl(np.float64('1.0'))
  std_ngv = sigma2_gyr_T1*np.sqrt(fs)
  print '    Tau = 1 crossing at:', sigma2_gyr_T1
  print '    Std Dev = ', std_ngv

  print '  Accel'
  sigma2_acc_lspl = interp1d(T, sigma2_acc, axis=1, copy=False)
  sigma2_acc_T1 = sigma2_acc_lspl(np.float64('1.0'))
  std_nav = sigma2_acc_T1*np.sqrt(fs)
  print '    Tau = 1 crossing at:', sigma2_acc_T1
  print '    Std Dev = ', std_nav

  #### compute markov time constant

  print 'Markov Time Constant:'

  print '  Gyro'
  acor_gyr0 = np.tile(acor_gyr[:,0].reshape((3,1)), (1,acor_gyr.shape[1]))
  taubg_idxs = np.argmax(acor_gyr < acor_gyr0*np.float64('0.368'), axis=1)
  taubg = np.array([acor_dt[i] for i in taubg_idxs])
  print '    Tau = ', taubg

  print '  Gyro'
  acor_acc0 = np.tile(acor_acc[:,0].reshape((3,1)), (1,acor_acc.shape[1]))
  tauba_idxs = np.argmax(acor_acc < acor_acc0*np.float64('0.368'), axis=1)
  tauba = np.array([acor_dt[i] for i in tauba_idxs])
  print '    Tau = ', tauba


  #### plotting

  win1 = pg.GraphicsWindow()
  fig11 = win1.addPlot(row=0, col=0)
  fig11.addLegend()
  fig11.setLabels(left='\sigma Gyro', bottom='\Tau')
  fig11.setLogMode(x=True, y=True)
  fig11.showGrid(x=True, y=True, alpha=0.5)
  fig12 = win1.addPlot(row=1, col=0)
  fig12.addLegend()
  fig12.setLabels(left='\sigma Accel', bottom='\Tau')
  fig12.setLogMode(x=True, y=True)
  fig12.showGrid(x=True, y=True, alpha=0.5)

  for i, pen, name in zip(range(3), (blue, green, red,), ('x', 'y', 'z')):
    fig11.plot(T, sigma_gyr[i,:], pen=pen, name=name)
    fig12.plot(T, sigma_acc[i,:], pen=pen, name=name)


  win2 = pg.GraphicsWindow()
  fig21 = win2.addPlot(row=0, col=0)
  fig21.addLegend()
  fig21.setLabels(left='Autocorr Gyro', bottom='\Delta t')
  # fig21.setLogMode(x=True, y=True)
  fig21.showGrid(x=True, y=True, alpha=0.5)
  fig21.setDownsampling(auto=True, mode='peak')
  fig21.setClipToView(True)  
  fig22 = win2.addPlot(row=1, col=0)
  fig22.addLegend()
  fig22.setLabels(left='Autocorr Accel', bottom='\Delta t')
  # fig22.setLogMode(x=True, y=True)
  fig22.showGrid(x=True, y=True, alpha=0.5)
  fig22.setDownsampling(auto=True, mode='peak')
  fig22.setClipToView(True)

  for i, pen, name in zip(range(3), (blue, green, red,), ('x', 'y', 'z')):
    fig21.plot(acor_dt, acor_gyr[i,:], pen=pen, name=name)
    fig22.plot(acor_dt, acor_acc[i,:], pen=pen, name=name)


  signal.signal(signal.SIGINT, sigint_handler)
  pg.QtGui.QApplication.instance().exec_()