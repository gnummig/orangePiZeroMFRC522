#!/usr/bin/env python
# -*- coding: utf8 -*-

import shelve
from pyA20.gpio import gpio
from pyA20.gpio import port
import MFRC522
import signal
from time import sleep
import sys
import select
import termios
import tty
from curses import ascii
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
#    gpio.cleanup()

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# configure gpio
gpio.init()
gpio.setcfg(18, gpio.OUTPUT)
gpio.output(18,1) # high means off 
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "RFID key registration and administration terminal."
print "Press \"h\" for help"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())
    while continue_reading:

        # open shelve to acces datastore
        ValidUIDs = shelve.open("UIDs.db", writeback=True)
        if isData():
            c = sys.stdin.read(1)
            outlist=[]
            for i in ValidUIDs:
                outlist.append(ValidUIDs[i])
            outlist.sort()
            if c== "h":
                print("usage:")
                print("p : print list of valid access")
                print("r : rename key")
                print("d : delete key")
            elif c=="p":
                print("registered cards")
                for name in outlist:
                    print(name)
            elif c=="r":
                print("rename card")
                name=raw_input("enter current name")
                if name in outlist:
                    newname=raw_input("enter new name")
                    for uid in ValidUIDs:
                        if ValidUIDs[uid]==name:
                            ValidUIDs[uid]=newname
                else:
                    print("not a card in my list")
            elif c=="d":
                print("delete card")
                name=raw_input("enter card name")
                if name in outlist:
                    for uid in ValidUIDs:
                        if ValidUIDs[uid]==name:
                            del ValidUIDs[uid]
                else:
                    print("not a card in my list")
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
            if UID in ValidUIDs:
                print("card belongs to:")
                print( ValidUIDs[UID])
            else:
                check=True
                while check:
                    newname=raw_input("enter name: ")
                    check=False
                    for number in ValidUIDs:
                        if newname==validUIDs[number]:
                            print("name exists, please choose a different")
                            check=True
                    if check==False:
                        ValidUIDs[UID]=newname
                        print "key: "+UID+" registered as "+ValidUIDs[UID]
    
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
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

