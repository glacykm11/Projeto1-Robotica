import vrep
import time
from sklearn import preprocessing

clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

if (clientID == 0):
  print('Conectado!')

c = 0
velocidade = 2 

#Motores 
returnC, motorEsquerdo = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
returnC, motorDireito = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)

#Sensores
returnC, sensor3 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor3',vrep.simx_opmode_oneshot_wait)
returnC, sensor4 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor4',vrep.simx_opmode_oneshot_wait)
returnC, sensor5 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor5',vrep.simx_opmode_oneshot_wait)
returnC, sensor6 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor6',vrep.simx_opmode_oneshot_wait)

#Acesso à câmera
returnC, camera = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)

#Leitura dos sensores como string
returnC, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor3,vrep.simx_opmode_streaming)
returnC, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor4,vrep.simx_opmode_streaming)
returnC, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor5,vrep.simx_opmode_streaming)
returnC, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor6,vrep.simx_opmode_streaming)

#Câmera
returnC, resolution, image = vrep.simxGetVisionSensorImage(clientID,camera,1,vrep.simx_opmode_streaming)

for i in range(200):
    returnC, detectionState, detectedPoint,detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor3,vrep.simx_opmode_buffer)
    returnC, detectionState, detectedPoint,detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor4,vrep.simx_opmode_buffer)
    returnC, detectionState, detectedPoint,detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor5,vrep.simx_opmode_buffer)
    returnC, detectionState, detectedPoint,detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor6,vrep.simx_opmode_buffer)

    returnC, resolution, image = vrep.simxGetVisionSensorImage(clientID,camera,1,vrep.simx_opmode_buffer)
    a = preprocessing.normalize(detectedPoint)
    if a > 0.01:
        print('Avançar')
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorDireito,velocidade,vrep.simx_opmode_blocking)
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorEsquerdo,velocidade,vrep.simx_opmode_blocking)
    if a > 0.01 & a < 0.75:
        print('Girar')
        for j in range (10):
            returnC = vrep.simxSetJointTargetVelocity(clientID,motorDireito,velocidade+1,vrep.simx_opmode_blocking)
            returnC = vrep.simxSetJointTargetVelocity(clientID,motorEsquerdo,velocidade,vrep.simx_opmode_blocking)
    else:
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorDireito,velocidade,vrep.simx_opmode_blocking)
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorEsquerdo,velocidade,vrep.simx_opmode_blocking)
    print(preprocessing.normalize(detectedPoint))
    time.sleep(0.1)

    vrep.simxFinish(-1)

vrep.delete()