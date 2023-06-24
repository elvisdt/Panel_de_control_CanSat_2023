import os 
import sys


#Agregar ruta actual del archivo
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)



import ahrs
from ahrs.common.orientation import q_prod, q_conj, acc2q, am2q, q2R, q_rot
import pyquaternion
import ximu_python_library.xIMUdataClass as xIMU
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ximu_python_library.xIMUdataClass as xIMU





# filePath = 'datasets/straightLine'
# startTime = 6
# stopTime = 26
# samplePeriod = 1/256

# filePath = 'datasets/stairsAndCorridor'
# startTime = 5
# stopTime = 53
# samplePeriod = 1/256

filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"datasets","spiralStairs")
#filePath = directorio_actual + "" +'datasets/spiralStairs'
startTime = 4
stopTime = 47
samplePeriod = 1/255



xIMUdata = xIMU.xIMUdataClass(filePath, 'InertialMagneticSampleRate', 1/samplePeriod)
time = xIMUdata.CalInertialAndMagneticData.Time
gyrX = xIMUdata.CalInertialAndMagneticData.gyroscope[:,0]
gyrY = xIMUdata.CalInertialAndMagneticData.gyroscope[:,1]
gyrZ = xIMUdata.CalInertialAndMagneticData.gyroscope[:,2]
accX = xIMUdata.CalInertialAndMagneticData.accelerometer[:,0]
accY = xIMUdata.CalInertialAndMagneticData.accelerometer[:,1]
accZ = xIMUdata.CalInertialAndMagneticData.accelerometer[:,2]

magX = xIMUdata.CalInertialAndMagneticData.magnetometer[:,0]
magY = xIMUdata.CalInertialAndMagneticData.magnetometer[:,1]
magZ = xIMUdata.CalInertialAndMagneticData.magnetometer[:,2]

indexSel = np.all([time>=startTime,time<=stopTime], axis=0)
time = time[indexSel]
gyrX = gyrX[indexSel]
gyrY = gyrY[indexSel]
gyrZ = gyrZ[indexSel]

accX = accX[indexSel]
accY = accY[indexSel]
accZ = accZ[indexSel]

magX = magX[indexSel]
magY = magY[indexSel]
magZ = magZ[indexSel]


# Compute accelerometer magnitude
acc_mag = np.sqrt(accX*accX+accY*accY+accZ*accZ)

# HP filter accelerometer data
filtCutOff = 0.001
b, a = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), 'highpass')
acc_magFilt = signal.filtfilt(b, a, acc_mag, padtype = 'odd', padlen=3*(max(len(b),len(a))-1))

# Compute absolute value
acc_magFilt = np.abs(acc_magFilt)

# LP filter accelerometer data
filtCutOff = 5
b, a = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), 'lowpass')
acc_magFilt = signal.filtfilt(b, a, acc_magFilt, padtype = 'odd', padlen=3*(max(len(b),len(a))-1))



# Threshold detection
stationary = acc_magFilt < 0.05

# Compute orientation
quat  = np.zeros((time.size, 4), dtype=np.float64)

# initial convergence
initPeriod = 2
indexSel = time<=time[0]+initPeriod
gyr=np.zeros(3, dtype=np.float64)
acc = np.array([np.mean(accX[indexSel]), np.mean(accY[indexSel]), np.mean(accZ[indexSel])])
mahony = ahrs.filters.Mahony(Kp=1, Ki=0,KpInit=1, frequency=1/samplePeriod)
q = np.array([1.0,0.0,0.0,0.0], dtype=np.float64)
for i in range(0, 2000):
    q = mahony.updateIMU(q, gyr=gyr, acc=acc)

# For all data
for t in range(0,time.size):
    if(stationary[t]):
        mahony.Kp = 0.5
    else:
        mahony.Kp = 0
    gyr = np.array([gyrX[t],gyrY[t],gyrZ[t]])*np.pi/180
    acc = np.array([accX[t],accY[t],accZ[t]])
    quat[t,:]=mahony.updateIMU(q,gyr=gyr,acc=acc)

# -------------------------------------------------------------------------
# Compute translational accelerations

# Rotate body accelerations to Earth frame
acc = []
for x,y,z,q in zip(accX,accY,accZ,quat):
    acc.append(q_rot(q_conj(q), np.array([x, y, z])))
acc = np.array(acc)
acc = acc - np.array([0,0,1])
acc = acc * 9.81

# Compute translational velocities
# acc[:,2] = acc[:,2] - 9.81

# acc_offset = np.zeros(3)
vel = np.zeros(acc.shape)
for t in range(1,vel.shape[0]):
    vel[t,:] = vel[t-1,:] + acc[t,:]*samplePeriod
    if stationary[t] == True:
        vel[t,:] = np.zeros(3)

# Compute integral drift during non-stationary periods
velDrift = np.zeros(vel.shape)
stationaryStart = np.where(np.diff(stationary.astype(int)) == -1)[0]+1
stationaryEnd = np.where(np.diff(stationary.astype(int)) == 1)[0]+1
for i in range(0,stationaryEnd.shape[0]):
    driftRate = vel[stationaryEnd[i]-1,:] / (stationaryEnd[i] - stationaryStart[i])
    enum = np.arange(0,stationaryEnd[i]-stationaryStart[i])
    drift = np.array([enum*driftRate[0], enum*driftRate[1], enum*driftRate[2]]).T
    velDrift[stationaryStart[i]:stationaryEnd[i],:] = drift

# Remove integral drift
vel = vel - velDrift

# -------------------------------------------------------------------------
# Compute translational position
pos = np.zeros(vel.shape)
for t in range(1,pos.shape[0]):
    pos[t,:] = pos[t-1,:] + vel[t,:]*samplePeriod

# -------------------------------------------------------------------------
# Plot 3D foot trajectory
posPlot = pos
quatPlot = quat

def getMagIMU():
    global magX, magY, magZ
    mag = np.column_stack((magX, magY, magZ))
    return mag

def getGyroIMU():
    global gyrX, gyrY, gyrZ
    gyro = np.column_stack((gyrX, gyrY, gyrZ))
    return gyro

def getAccIMU():
    global accX, accY, accZ
    mag = np.column_stack((accX, accY, accZ))
    return mag

def getAccLin():
    global acc
    return acc

def getVelLin():
    global vel
    return vel

def getPosLin():
    global posPlot
    return posPlot


if __name__ == "__main__":
    print(getMagIMU().shape)
    print(getGyroIMU().shape)
    print(getAccIMU().shape)

    print(getAccLin().shape)
    print(getVelLin().shape)
    print(getPosLin().shape)

