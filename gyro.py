#basic script for testing the Gyro, troubleshooting or trying things to see what it can do, and what data it provides.

import time
import board
import busio
from adafruit_lsm6ds import LSM6DS33

i2c = busio.I2C(board.SCL, board.SDA)
sensor = LSM6DS33(i2c)

#importing complete for the sensor, at this point. can then get acceleration or Gyro info.
#acceleration is forces in X, Y, Z, in m/s^2
#Gyro is rotation on the X, Y, Z axes in Degrees/Sec

#To print to screen:
while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
    print("")
    time.sleep(0.5)
