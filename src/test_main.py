import ahrs
from ahrs.common.orientation import q_prod, q_conj, acc2q, am2q, q2R, q_rot
import pyquaternion
import ximu_python_library.xIMUdataClass as xIMU
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



from pykalman import KalmanFilter

# filePath = 'datasets/straightLine'
# startTime = 6
# stopTime = 26
# samplePeriod = 1/256

# filePath = 'datasets/stairsAndCorridor'
# startTime = 5
# stopTime = 53
# samplePeriod = 1/256


import os

current_path = os.getcwd()
print(current_path)

filePath = 'D:/Archivos EJD/PROYECTO CANSAT/DISEÑO DE PANEL DE CONTROL/Panel_de_control_CanSat/data/data_1.csv'
startTime = 4
stopTime = 47
samplePeriod = 1/256


xIMUdata = xIMU.xIMUdataClass(filePath, 'SampleRate', 1/samplePeriod)
time = xIMUdata.CalInertialAndMagneticData.Time
gyrX = xIMUdata.CalInertialAndMagneticData.gyroscope[:,0]
gyrY = xIMUdata.CalInertialAndMagneticData.gyroscope[:,1]
gyrZ = xIMUdata.CalInertialAndMagneticData.gyroscope[:,2]
accX = xIMUdata.CalInertialAndMagneticData.accelerometer[:,0]
accY = xIMUdata.CalInertialAndMagneticData.accelerometer[:,1]
accZ = xIMUdata.CalInertialAndMagneticData.accelerometer[:,2]

#solo se ejecutara entre un rango de tiempo
indexSel = np.all([time>=startTime,time<=stopTime], axis=0)
time = time[indexSel]
gyrX = gyrX[indexSel]
gyrY = gyrY[indexSel]
gyrZ = gyrZ[indexSel]
accX = accX[indexSel]
accY = accY[indexSel]
accZ = accZ[indexSel]

print(len(accX))