# CREATED BY AVE
# UPLOADED 3/22/18 TO GITHUB BY JESSICA COHEN
# Connects to Bluetooth device with matching UUID
# Being used to connect with Android device
# Run on Raspberry Pi 3 Model B

import os
import bluetooth
import socket
import RPi.GPIO as GPIO
import time
from bluetooth import *

connection = False
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

#unique UUID to connect with AVE Android Phone
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AVECCPDataServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ]
						 )
while True:
	if(connection == False):
		print("Waiting for connection on RFCOMM channel %d" % port)
		client_sock, client_info = server_sock.accept()
		connection = True
		print("Accepted connection from ", client_info)
	try:
            data = client_sock.recv(1024)
            if (data == "disconnect"):
                print("Client wanted to disconnect")
                client_sock.close()
                connection = False
					 
				# this is the string that AVE is sending to RP3
            elif (data == "AVE test data!!"):
		print ("The Android App just sent: %s" % data)
					# Printing for testing 
                print ("Fake Data is being sent here!")
					 # this string is what RP3 sends to AVE
                testData = "Velocity: 123"
					 # sends string to AVE
                client_sock.send("RECEIVED: %s" % testData)
					# Printing for testing 
                print("SENT: %s" % testData)
	    
	except IOError:
            print("Connection disconnected!")
            client_sock.close()
	    connection = False
	    pass
	except BluetoothError:
		print("Something wrong with bluetooth")
	# this may have to be changed in the future
	# (it may be causing issues with continuous connection)
	except KeyboardInterrupt:
		print("\nDisconnected")
		client_sock.close()
		server_sock.close()
		break

