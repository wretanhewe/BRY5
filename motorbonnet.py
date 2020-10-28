# Basic script for testing out functions on the motors, to get them turning with the motor bonnet.
from adafruit_motorkit import MotorKit
kit = MotorKit(i2c=board.I2C())
#throttle, is how we can set the "Speed". 1.0 is Full Speed, however much that is for the motor.
#to go other direction, use a negaive value.
#stop the motor with a 0
#motor is wired between M1 (or M2, M3, or M4) and Ground. Call out appropriate motor here, with
kit.motor1.throttle = 1.0
