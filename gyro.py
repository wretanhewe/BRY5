#basic script for testing the Gyro, troubleshooting or trying things to see what it can do, and what data it provides.
import time
import board
import busio
import adafruit_mpu6050

i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

#importing complete for the sensor, at this point. can then get acceleration or Gyro info.
#acceleration is forces in X, Y, Z, in m/s^2
#Gyro is rotation on the X, Y, Z axes in Degrees/Sec

#To print to screen:
while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    print("Temperature: %.2f C" % mpu.temperature)
    print("")
    time.sleep(1)
