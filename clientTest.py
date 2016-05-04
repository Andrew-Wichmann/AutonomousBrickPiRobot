
import paramiko
import sys
import time
from BrickPi import *   #import BrickPi.py file to use BrickPi operations

#usage: python clientTest.py command(move) seconds(10)
# motor A: lifter, B: right wheel, C: left wheel

if len(sys.argv) > 1:
  arg1 = sys.argv[1]
else:
  print("No command given")
if len(sys.argv) > 2:
  arg2 = float(sys.argv[2])
else:
  print("No arg2 Given, setting to 1")
  arg2 = 1

#Set up the SSH connect from robot to server
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.43.99', username='pi', password='robots1234')
sftp=ssh.open_sftp()
f=sftp.open("/home/pi/Documents/finder.log",mode='a')

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
BrickPi.MotorEnable[PORT_C] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor B   #Send the properties of sensors to BrickPi
BrickPiUpdateValues()
power = 0


def lift(seconds):
  print("lifting")
  power = -150
  BrickPi.MotorSpeed[PORT_A] = power  #Set the speed of MotorA (-255 to 255)
  ot = time.time()
  while(time.time() - ot < seconds):    #running while loop for .25 seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors

def drop(seconds):
  print("dropping")
  power = 150
  BrickPi.MotorSpeed[PORT_A] = power  #Set the speed of MotorA (-255 to 255)
  ot = time.time()
  while(time.time() - ot < seconds):    #running while loop for .17 seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors


def fwd(seconds):
  power = 50.0
  BrickPi.MotorSpeed[PORT_C] = 60   #Set the speed of MotorA (-255 to 255)
  ot = time.time()
  while(time.time() - ot < seconds):    #running while loop for "arg2" seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
  BrickPi.MotorSpeed[PORT_B] = 0  #Set the speed of MotorA (-255 to 255)
  #BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()

def back(seconds):
  power =50.0
  BrickPi.MotorSpeed[PORT_C] = -180   #Set the speed of MotorA (-255 to 255)
  ot = time.time()
  while(time.time() - ot < seconds):    #running while loop for "arg2" seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
  BrickPi.MotorSpeed[PORT_B] = 0  #Set the speed of MotorA (-255 to 255)
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()

def start():
  found = True
  f.write("seeking")
  BrickPi.SensorType[PORT_4] = TYPE_SENSOR_EV3_US_M0
  BrickPiSetupSensors()
  result = 65001
  timer = time.time()
  while (result > 65000):
    result = BrickPi.Sensor[PORT_4]
    if (time.time() - timer > 2):
      BrickPi.SensorType[PORT_4] = TYPE_SENSOR_EV3_US_M0
      BrickPiSetupSensors()
      BrickPiUpdateValues()
      timer = time.time()

  BrickPi.MotorSpeed[PORT_C] = 45
  result = 1000
  desiredvalue = 40
  ot = time.time()
  while (result > desiredvalue):
    if ((time.time() - ot) > 15):
      f.write("round over")
      break
      found = False
    error = BrickPiUpdateValues()
    if not error :
      if (BrickPi.Sensor[PORT_4] > 0):
        result = BrickPi.Sensor[PORT_4]
        print str(result)
  split = time.time() - ot
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  time.sleep(1)
  BrickPi.MotorSpeed[PORT_C] = -45
  nt = time.time()
  while (time.time() - nt < split):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  if found:
    f.write("found")
    outsplit = str(split)
    time.sleep(.1)
    f.write(outsplit)
    print(outsplit)

def retrieve(split):
  f.write("retrieving")
  wheelpower = 55
  BrickPi.MotorSpeed[PORT_C] = wheelpower
  ot = time.time()
  while (time.time() - ot < (split + .1)):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_B] = -50
  oot = time.time()
  while (time.time() - oot < .7):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_B] = 0
  BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = -wheelpower
  nt = time.time()
  while (time.time() - nt < (split + .1)):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_B] = 50
  ooot = time.time()
  while (time.time() - ooot < .7):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_B] = 0
  BrickPiUpdateValues()
  #BrickPi.MotorSpeed[PORT_C] = -70
  rt = time.time()
  while (time.time() - rt < 2):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  print ("object retrieved")
  f.write("object retrieved")

def colorFind(split):
  f.write("determining color")
  BrickPi.SensorType[PORT_4] = TYPE_SENSOR_EV3_COLOR_M2   #Set the type of sensor at PORT_4.  M2 is color.
  BrickPiSetupSensors()
  BrickPiUpdateValues()
  found = False 
  BrickPi.MotorSpeed[PORT_C] = 45
  ot = time.time()
  while (time.time() - ot < split):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  inchForward=0
  timer = time.time()
  while not found:
	result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors 
        gyro = BrickPi.Sensor[PORT_4]
	if gyro is 5:
		print "RED"
                color = "RED"
                found = True
	if gyro is 2:
		print "BLUE"
                color = "BLUE"
                found = True
        if (time.time() - timer > 2):
          inchForward = inchForward+1
          print inchForward
          if((inchForward%3) == 1):
            BrickPi.MotorSpeed[PORT_C] = 13
            timer1=time.time()
            while(time.time() - timer1<1):
              BrickPiUpdateValues()
            BrickPi.MotorSpeed[PORT_C] = 0
            BrickPiUpdateValues()
          BrickPi.SensorType[PORT_4] = TYPE_SENSOR_EV3_COLOR_M2   #Set the type of sensor at PORT_4.  M2 is color.
          BrickPiSetupSensors()
          BrickPiUpdateValues()
          timer = time.time()
  BrickPi.MotorSpeed[PORT_C] = -45
  nt = time.time()
  while (time.time() - nt < split):
    BrickPiUpdateValues()
  BrickPi.MotorSpeed[PORT_C] = 0
  BrickPiUpdateValues()
  print ("done")
  f.write("found color")
  time.sleep(1)
  f.write(color)

if __name__ == "__main__":
  if arg1 == "start":
    start()
  if arg1 == "retrieve":
    retrieve(arg2)
  if arg1 == "colorFind":
    colorFind(arg2)
  if arg1 == "lift":
    lift(arg2)
  if arg1 == "drop":
    drop(arg2)
  if arg1 == "back":
    back(arg2)
  if arg1 == "fwd":
    fwd(arg2)
