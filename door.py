#!/usr/bin/env python
# -*- coding: utf8 -*-

#import shelve
import csv
from pyA20.gpio import gpio
from pyA20.gpio import port
import MFRC522
import os
import signal
from time import sleep, time , ctime

OPEN = 0
CLOSED = 1

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
def door(dstate):
    gpio.output(18,dstate)
def beep(beeplength):
    gpio.output(12,1)   # beep
    sleep(beeplength)
    gpio.output(12,0)

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# configure gpio
gpio.init()
# relais:
gpio.setcfg(18, gpio.OUTPUT)
door(CLOSED)
# beeper:
gpio.setcfg(12, gpio.OUTPUT)
gpio.setcfg(10,gpio.INPUT)
gpio.pullup(10,gpio.PULLUP)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."
admin = 0
lastopen = 0
admintime = 0
registermode = 0
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # there is a manual switch connected to pin 10
    if gpio.input(10)==0:
        door(OPEN)
        sleep(3)
        door(CLOSED)

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if registermode and time() > admintime +10:
        registermode = False
	print " exiting register mode"		
    if status == MIFAREReader.MI_OK:
    
        UID=str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        # check for register mode:
        # MFRCC gets strange reads if reading twice in one while loop
        print time()
        print lastopen
        print admin
        if registermode:
            if oldUID != UID:
                # dooraccess : name , UID , valid until date , registered date
                dooraccess.append( [ card [ 0 ] + "_guest_key" , UID , time ( ) + 3600*24*14 , ctime()] )
                print [ card [ 0 ] + "_guest_key" , UID , time ( ) + 3600*24*14 , ctime()]
                with open ( 'dooraccess' , 'w' ) as writefile:
                    writer = csv.writer ( writefile )
                    writer.writerows( dooraccess )
                #os.system('sync_doors.sh')
                beep(1)
            lastopen = time()
        elif time() < lastopen + 3 and admin and oldUID == UID:
            # if admin ard is read for longer than 5 seconds a second card can be registered
            print "entering register mode"
            beep(0.125)
            sleep(0.125)
            beep(0.125)
            admintime = time()
            registermode = True

        else:
            # Print UID
            print "Card read UID: "+UID

            # open csv on each request to have recent database
            with open ('dooraccess' , 'r' ) as readfile:
                reader = csv.reader ( readfile )
                dooraccess = list(reader)
                ValidUids = []
            with open ('dooradmin'  , 'r' ) as readfile:
                reader = csv.reader ( readfile )
                dooradmin = list(reader)
                ValidUids = []

            # check for the UID in the two tables
            for line in dooraccess:
                if line [2] < time():
                    dooraccess.remove(line)
                    continue;
                if line [1] == UID:
                    card = line
                    break;
                else: card = False
            admin = False
            for line in dooradmin:
                if line[1] == UID:
                    card = line
                    admin = True
            if card:
                print card [ 0 ]
                if admin : print "admin"
                door(OPEN)
                beep(0.2)
                sleep(5)
                door(CLOSED)
                print "door closed"
                lastopen = time()
                oldUID=UID

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



