import time
import sys
import paramiko

if len(sys.argv) > 1:
	target= sys.argv[1]
	target = target.upper()
	print "Server: Seeking", target
else:
	print "No target given"
rowLength = 20
numOfRows = 5

def setupSSH():
	#Set up SSH connection from server to robot
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('192.168.43.127', username='pi', password='robots1234')
	return ssh	

def setupLogFile():
	#Erase the log file
	g = open('finder.log', 'w')
	g.close()
	f = open('finder.log', 'r')
	return f

def setupOLs():
	#Initialize object location array
	objectLocations=[[0 for j in range(rowLength)] for i in range(numOfRows)]
	return objectLocations

def sendRetrieval(distance):
	print distance
	command = 'python /home/pi/Desktop/CS404Spring2016/clientTest.py retrieve %s' % distance
	print command
	ssh.exec_command(command)

def pickUpObjects(i,j):
	raw_input("Server: Please place the arm on the robot. Press Enter to continue.")
	k=0
	while (objectLocations[i][k] != 0):
		print ("Picking up object ", i)
		sendRetrieval(objectLocations[i][k])
		k = k+1
		if (k == rowLength):
			break
def start():
	seek()

def seek():
	command = 'python /home/pi/Desktop/CS404Spring2016/clientTest.py start'
	print "Server: Sending command:",command
	ssh.exec_command(command)

#################################################################
#End of function declarations#
#################################################################
#################################################################
#Start of setup#
#################################################################
print "Server: Setting up data structures"
objectLocations=setupOLs()
f = setupLogFile()
print "Server: Setting up SSH tunnel"
ssh = setupSSH()

#################################################################
#End of setup#
#################################################################
#################################################################
#Start of server body#
#################################################################


incomplete = 1
split=0
objectsRetrieved=0
i=0
j=0
print "Server: Starting"

#Start the robot
start()

#Start the server loop
while(incomplete):
	time.sleep(.1)
	line = f.readline()
	if line != "":
		print line
		if line == "found":
			raw_input("Server: Place color sensor on robot. Press Enter to continue.")
			time.sleep(1)
			split=f.readline()
			command = 'python /home/pi/Desktop/CS404Spring2016/clientTest.py colorFind %s' % split
			print "Server: Sending command:",command
			ssh.exec_command(command)
		elif line == "found color":
			line = f.readline()
			while(line == ""):
					line=f.readline()
			if (line == target):
				print 'Server: Found color ',line
				raw_input("Server: Place pusher on robot. Press Enter to continue.")	
				time.sleep(1)
				command = 'python /home/pi/Desktop/CS404Spring2016/clientTest.py retrieve %s' % split
				print 'Server: Sending command:',command
				ssh.exec_command(command)
				objectLocations[i][j] = split
				j=j+1
			else:
				print "Didn't find",target," found", line
				raw_input("Server: Place ultrasonic on robot. Press Enter to continue.")
				seek()
		elif line == "object retrieved":
			objectsRetrieved = objectsRetrieved +1
			print "Server: Retrieved",objectsRetrieved,"objects so far"
			raw_input("Server: Place ultrasonic on robot. Press Enter to continue.")
			seek()
		elif line == "round over":
			#server tells robot to pick up objects in row i
			raw_input("Place robot on the next row. Press Enter to continue.")
			#increments i (row)
			i=i+1
			#exit server loop if no more rows to search/pick up
			if (i == (numOfRows+1)):
					incomplete = 0
print ("Server: Finished! Grade A please!")
#################################################################
#End of server body#
#################################################################
