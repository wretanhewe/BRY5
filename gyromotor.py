#Basic config to control motor speed and left/right based on gyro position in space
#using simple-pid for PID loop. https://pypi.org/project/simple-pid/
#DC Motor at only 5 volts seems to be unable to turn freely if its given a signal less than 0.4, when it's at a full stop already.

import time
import board
import busio
from simple_pid import PID #get PID functions.
from numpy import interp #interpolation for number scale mapping
import adafruit_mpu6050 #for gyro
from adafruit_motorkit import MotorKit #for motors

kit = MotorKit(i2c=board.I2C())
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
pid=PID(0.2,0.0,0.0, setpoint=0) #P,I,D gains and setpoint.
#Kp affects how fast things respond. BAsed on where PV IS, and where SP needs it to be, and how far that is.
#Ki Sums error difference, integral increases over time, until steady-state. even small error will make this term rise slowly over time.
#Kd Makes the output decrease if PV is increasing FAST. Increading this paramter will make it react stronger to changes in Error. SHould be small.

pid.output_limits = (-1,1) #set limits, since output to motor speed only go 0 to 1 anyway, in either direction
#mpu.acceleration is an array of x, y, z accleration values. Zero-indexed one dimensional array(?)
#reference elements with a square bracket.

#set motor to 0 throttle.
#kit.motor1.throttle = 0
#kit.motor3.throttle = 0

while True:
    print(mpu.acceleration[1])
    motorturn=pid(mpu.acceleration[1]) #PID tries to get the X acceleration to 0, established above. The outputis the speed of the motor.
    #print(motorturn)
    kit.motor1.throttle = motorturn
    kit.motor3.throttle = -motorturn #reversed direction, because motor is moving "other" way
    #time.sleep(0.1)
