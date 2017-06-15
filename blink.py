#!/usr/bin/env python
# -*- coding: utf8 -*-

from pyA20.gpio import gpio
from time import sleep

# configure gpio
gpio.init()
gpio.setcfg(18, gpio.OUTPUT)
gpio.output(18,1) # high means off 
while 1:
    gpio.output(18,0)
    sleep(0.5)
    gpio.output(18,1)
    sleep(0.5)
    print "test"
