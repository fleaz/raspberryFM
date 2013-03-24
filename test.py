#! /usr/env/python

import lib.raspFM
import smbus

bus = smbus.SMBus(0)
fm = raspFM.ns741(bus,0x66,102000)

fm.init_module()
fm.set_power_state(2)
