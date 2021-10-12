import vrep
import time
import numpy as np

clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

if (clientID == 0):
  print('Conectado!')

c = 0
velocidade = 1

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
returnC, detectionState, detectedPoint3, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor3,vrep.simx_opmode_streaming)
returnC, detectionState, detectedPoint4, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor4,vrep.simx_opmode_streaming)
returnC, detectionState, detectedPoint5, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor5,vrep.simx_opmode_streaming)
returnC, detectionState, detectedPoint6, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor6,vrep.simx_opmode_streaming)

#Câmera
returnC, resolution, image = vrep.simxGetVisionSensorImage(clientID,camera,1,vrep.simx_opmode_streaming)

for i in range(200):
    
    returnC, detectionState, detectedPoint3, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor3,vrep.simx_opmode_buffer)
    returnC, detectionState, detectedPoint4, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor4,vrep.simx_opmode_buffer)
    returnC, detectionState, detectedPoint5, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor5,vrep.simx_opmode_buffer)
    returnC, detectionState, detectedPoint6, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,sensor6,vrep.simx_opmode_buffer)

    returnC, resolution, image = vrep.simxGetVisionSensorImage(clientID,camera,1,vrep.simx_opmode_buffer)
    a3 = np.linalg.norm(detectedPoint3)
    a4 = np.linalg.norm(detectedPoint4)
    a5 = np.linalg.norm(detectedPoint5)
    a6 = np.linalg.norm(detectedPoint6)

    print("a3: ", a3)
    print("a4: ", a4)
    print("a5: ", a5)
    print("a6: ", a6)

    if ((a3 >= 0.1) & (a3 < 0.75)) | ((a4 >= 0.1) & (a4 < 1)):
        print('Girar Direita')
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorDireito,velocidade+1,vrep.simx_opmode_blocking)
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorEsquerdo,velocidade,vrep.simx_opmode_blocking)
    if ((a5 >= 0.1) & (a5 < 1)) | ((a6 >= 0.1) & (a6 < 1)):
        print('Girar Esquerda')
        # for j in range (20):
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorDireito,velocidade, vrep.simx_opmode_blocking)
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorEsquerdo,velocidade+1,vrep.simx_opmode_blocking)
    else:
        print('Avançar')
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorDireito,velocidade,vrep.simx_opmode_blocking)
        returnC = vrep.simxSetJointTargetVelocity(clientID,motorEsquerdo,velocidade,vrep.simx_opmode_blocking)

    time.sleep(1)



