#!/usr/bin/env python
# -*- coding: utf8 -*-

import shelve
from pyA20.gpio import gpio
from pyA20.gpio import port
import MFRC522
import signal
from time import sleep


continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
#    gpio.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# configure gpio
gpio.init()
gpio.setcfg(18, gpio.OUTPUT)
gpio.output(18,1) # high means off 
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        UID=str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        print "Card read UID: "+UID
        # open shelve to acces datastore
        ValidUIDs = shelve.open("UIDs.db", writeback=True)
        if UID in ValidUIDs:
            print("acces granted to ")
            print( ValidUIDs[UID])
            gpio.output(18,0)
            sleep(5)
            gpio.output(18,1)
            print "door closed"

        # This is the default key for authentication
        #key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        # Select the scanned tag
        #MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        #status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        #if status == MIFAREReader.MI_OK:
        #    MIFAREReader.MFRC522_Read(8)
        #    MIFAREReader.MFRC522_StopCrypto1()
        #else:
        #    print "Authentication error"



