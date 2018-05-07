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

while(connection == False):
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    #unique UUID to connect with AVE Android Phone
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    file = open("CCPtoAVE_Data.txt", "r")

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
                    for aline in file:
                            client_sock.send(aline);
                            print("String that was just sent: %s" % aline)
                            
                            # Receive data back from AVE:
                            data = client_sock.recv(1024)
                            stop,lon,lat,errcount=data.split(",")
          
                        
                            
                            print("Stopwatch: %s" % stop)
                            print("Received Longitude: %s" % lon)
                            print("Received Latitude: %s" % lat)
                            print("Error Count: %s" % errcount)

                    
                                    
                                    # data = client_sock.recv(1024)
                # if (data == "disconnect"):
                    # print("Client wanted to disconnect")
                    # client_sock.close()
                    # connection = False
                                             
                                    # # this is the string that AVE is sending to RP3
                # elif (data == "AVE test data!!"):
                    # print ("The Android App just sent: %s" % data)
                                            
                                             # for aline in file:
                                                    # client_sock.send(aline);
                                                    # print("String that was just sent: %s" % aline)
                                                    
                                                    # # Receive data back from AVE:
                                                    # data = client_sock.recv(1024)
                                                    # values = data.split()
                                                    # lat = values[0]
                                                    # long = values[1]
                                                    
                                                    # print("Received Latitude: %s" % lat)
                                                    # print("Received Longitude: %s" % lon)
                                                    
                                             
                                             # # # this string is what RP3 sends to AVE
                    # # testData = "Straight,Forward,27,36,-2"
                                             # # # sends string to AVE
                    # # client_sock.send("RECEIVED: %s" % testData)
                                            # # # Printing for testing 
                    # # print("SENT: %s" % testData)
            
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
            server_sock.close()

