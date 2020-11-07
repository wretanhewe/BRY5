#!/usr/bin/env python3
import time
import board
import busio
import multiprocessing
import queue
import adafruit_mpu6050
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper #stepper functionality, for doing stepper motors. I think we have to include this?
from simple_pid import PID


i2c = busio.I2C(board.SCL, board.SDA)
kit = MotorKit(i2c=board.I2C())
mpu = adafruit_mpu6050.MPU6050(i2c)
pid = PID(8,0,0, setpoint=0)   # PID loop to balance to zero

pid.output_limits = (-100, 100) #range is limited up to "100%"

global motorpercent #initialize the global
oneshot=0   #debugging variable.
motorsleep = 1 #initialize sleeptime. High number means slow speed/no movement.

#this is code for the child process.
def wheelbalance(conn):
    while True: #This may not be the best way to loop, but... best I have for now.
#        try:
#            pulse=conn.get() #this will receive the queue data into Pulse variable for this function
#            print("queue Has Data")
#        except:
#            print("queue is empty")
#            pass

        pulse=conn.get()

        #pulse=0 #setting this static to test the motors.

        print("pulse is", pulse) #debugging.
        steps=10 #do more than one step for smoothness.
        #for i in (1000): #I dont want to make while TRUe, because runaway process? will find a way for this later.
        #Dont turn motors if it's fallen over.
        if abs(mpu.acceleration[1]) > 8:
            kit.stepper1.release()
            kit.stepper2.release()
        elif mpu.acceleration[1] > 0: #direction setting here. adjust based on wiring.
            for i in range(steps): #do a few steps
                kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
                kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
                time.sleep(pulse)
        else:
            for i in range(steps): #do a few steps
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
                kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
                time.sleep(pulse)


#start the second process, to run the stepper motors:
queue = multiprocessing.Queue() #setup queue to send info.
wheelcontrol = multiprocessing.Process(target=wheelbalance, args=(queue,))
wheelcontrol.start() #starts this child process. How does it stop?


###########
#The main code here:
###########

while oneshot<100000:
    #first check PID and get values
    motorpercent = pid(mpu.acceleration[1]) #global so that the wheel process can see this
    motorsleep = 0.01-(abs(motorpercent)/10000)

    #send new timing value to the child process, for motor control.
    if oneshot < 100000:
        queue.put(motorsleep)
        oneshot = oneshot+1 #so this if won't run again.
        print("sending...")

    #print for debugging:
    #print(mpu.acceleration[1])
    #print(motorpercent)
    #print(motorsleep)

    #time.sleep(1) #general sleep for the main process to slow down, and print etc.
