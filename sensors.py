import sys, os
import pyproj as proj4
from numpy import array, float64, nan
from numpy import diff, unique, sqrt, diag, diagflat, power, deg2rad, mean, rad2deg, zeros, hstack, std, cov, arctan2, ones, vstack, allclose, arange, round, eye
from scipy.linalg import block_diag
import simplekml
import chroma
import utm
from ipdb import set_trace


# __all__ = ['IMUNoise', 'IMUEpoch', 'GPSEpoch']


class IMUNoise(object):
  """Representation of IMU noise characteristics using spec sheet data
  """
  
  fields = (
    'taubg',
    'tauba',
    'gyro_bias',
    'accel_bias',
    'angular_random_walk',
    'velocity_random_walk',
    'gyro_scale',
    'accel_scale',
    'gyro_static_std',
    'accel_static_std',
  )
  
  def __init__(self, **kwargs):
    """kwargs must be what's specified in `fields`. Nothing more or less.
    :param float taubg:
    :param float tauba:
    :param float gyro_bias:
    :param float accel_bias:
    :param float angular_random_walk:
    :param float velocity_random_walk:
    :param float gyro_scale:
    :param float accel_scale:
    :param float gyro_static_std:
    :param float accel_static_std:
    """
    missing_fields = set(self.fields) - set(kwargs.keys())
    if len(missing_fields) > 0:
      raise Exception('Missing fields: ')
    for kwarg in kwargs:
      if kwarg not in self.fields:
        raise Exception("unknown field: "+kwarg)
      setattr(self, kwarg, kwargs[kwarg])

    # set the fundamental entities in __init__ so they can be manipulated later
    # on if need be, before calculating `Q`

    ## White noise on the measurements
    # ngv_std = angular_random_walk / sqrt(tau_bgd)
    # nav_std = velocity_random_walk / sqrt(tau_bad)
    self.ngv_std = self.gyro_static_std
    self.nav_std = self.accel_static_std
    ## White noise on the bias time derivative
    # ngu_std = gyro_bias
    # nau_std = accel_bias
    self.ngu_std = self.angular_random_walk / self.taubg**1.5
    self.nau_std = self.velocity_random_walk / self.tauba**1.5

  def input_noise_covariance(self, rbpf=False):
    """Generate `Q` for the LC formulation in derivations corresponding to the 
    covariance of the vector `n`
    """
    return diagflat(vstack((
      self.ngv_std**2 * ones((3,1)),
      self.ngu_std**2 * ones((3,1)),
      self.nav_std**2 * ones((3,1)),
      self.nau_std**2 * ones((3,1)),
    )))



class XBow440Noise(IMUNoise):
  """Crossbow IMU440CA-200
  """
  def __init__(self):
    super(XBow440Noise, self).__init__(
      taubg = 800., # cody
      tauba = 600., # cody
      gyro_bias = deg2rad(0.75), # rad/s # this is the limit on the bias given by the spec sheet
      accel_bias = 15.0 * 9.81 / 1000., # m/s^2 # this is the limit on the bias given by the spec sheet
      angular_random_walk = deg2rad(4.5) / 60., # rad / sqrt(s)
      velocity_random_walk = 1.0 / 60., # m/s / sqrt(s)
      gyro_scale = 0.01,
      accel_scale = 0.01,
      # gyro_static_std = 0.0022, # see `characterize_imu.py` # this should be automated from the output `ic_std`
      # accel_static_std = 0.0063, # see `characterize_imu.py` # this should be automated from the output `ic_std`
      gyro_static_std = 0.022,
      accel_static_std = 0.063,
    )


class IMUEpoch(object):
  
  def __init__(self, mdw_time, gx, gy, gz, ax, ay, az):
    self.mdw_time = mdw_time
    self.gyr = array([gx, gy, gz]).reshape((3,1))
    self.acc = array([ax, ay, az]).reshape((3,1))


