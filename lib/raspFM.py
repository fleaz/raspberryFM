import smbus
from time import sleep

TX_BIT = 0x01
OSCILLATOR_BIT = 0x02
MUTE_BIT = 0x01
RF_POWER_BIT_0 = 0x40
RF_POWER_BIT_1 = 0x80
ALC_AUTO = 0x01
MAA_SET = {1:7, 2:6, 3:5, 4:4, 5:4, 6:3, 7:3, 8:2, 9:2, 10:1, 11:1, 12:1, 13:1, 14:0}

class ns741:

    def __init__(self, i2cbus,  address, frequency):
        #address of device, normal is 0x66 for that device
        self._address = address
        #frequency whrere will be transmitted
        self._frequency_kHz = frequency
        #bus used for controling the transmitter
        self._bus = i2cbus
        #strange things, this seems something for tuning... 
        self._p2 = 0xE7E  
        #transmit power currently set
        self._transmit_power=0

    def i2c_write(self,  start_register,  val_field):
        try:
            self._bus.write_i2c_block_data(self._address, start_register , val_field)
        except IOError, err:
            return self.errMsg()        

    def i2c_read_register(self,  reg):
        try:
            ret_val = self._bus.read_i2c_block_data(self._address, 0x00 , reg+1)[reg]
        except IOError, err:
            return self.errMsg()       
        return(ret_val)

    def init_modul(self):
        #that are the default values as discribt in the datasheet of Alps tuner.
        #this have to be written to the registeres 0x00 to 0x16
        init_data = [0x02, 0x83, 0x0A, 0x00,
                     0x00, 0x00, 0x00, 0x7E,
                     0x0E, 0x08, 0x3F, 0x2A,
                     0x0C, 0xE6, 0x3F, 0x70,
                     0x0A, 0xE4, 0x00, 0x42,
                     0xC0, 0x41, 0xF4]


        #first resetting the modul
        self.reset()

        #writeing init data
        self.i2c_write(0x00, init_data)       

        #wait 700ms for stabilize the crystal oscillation
        sleep(0.7)
        #switch power on(PE to ON)
        self.set_power_state(True)        
        #wait 150ms 
        sleep(0.15)
        #FIXME: Set ALC to ON

        #set freqency
        self.set_frequency(self._frequency_kHz)
        
        #i do not know why, but we have to write there to start transmitting.... not dokumentaed?! WTF?
        self.i2c_write(0x10,  [0x20])
        
        #FIXME: start rds transmit

    def reset(self):
        #this method resets the transmitter
        self.i2c_write(0x7F,  [0xA0])


    def set_power_state(self,  state):
        #this method is used for switching power state of the module

        #get state of register 00 where power bit is
        register_00 = self.i2c_read_register(0x00)

        if (state == True) and (register_00 & TX_BIT == 0) :
            self.i2c_write(0x00, [register_00 | TX_BIT])
        elif(state == False) and (register_00 & TX_BIT != 0) :
            self.i2c_write(0x00, [register_00 & ~TX_BIT])
        else:
            print ("it already had the suggested power state" + " " + str(register_00) )

    def set_ALC_state(self,  state):
        #this method is used for switching Auto Level Control auto state of the module

        #get state of register 00 where power bit is
        register_0D = self.i2c_read_register(0x0D)

        if (state == True) and (register_0D & ALC_AUTO == 0) :
            self.i2c_write(0x00, [register_0D | ALC_AUTO])
        elif(state == False) and (register_0D & ALC_AUTO != 0) :
            self.i2c_write(0x00, [register_0D & ~ALC_AUTO])
        else:
            print ("it already had the ALC auto state" + " " + str(register_0D) )

    def set_oscillator_state(self,  state):
        #this method is used for switching oscillator state of the module

        #get state of register 00 where oscillator bit is
        register_00 = self.i2c_read_register(0x00)

        if (state == True) and (register_00 & OSCILLATOR_BIT == 0) :
            self.i2c_write(0x00, [register_00 | OSCILLATOR_BIT])
        elif(state == False) and (register_00 & OSCILLATOR_BIT != 0) :
            self.i2c_write(0x00, [register_00 & ~OSCILLATOR_BIT])
        else:
            print ("it already had the suggested oscillator state" + " " + str(register_00) )


    def set_mute(self,  state):
        # this method is used for muting audio transmission

        #get state of register 02 where mute bit is
        register_02 = self.i2c_read_register(0x02)

        if (state == True) and (register_02 & MUTE_BIT == 0) :
            self.i2c_write(0x02, [register_02 | MUTE_BIT])
        elif(state == False) and (register_02 & MUTE_BIT != 0) :
            self.i2c_write(0x02, [register_02 & ~MUTE_BIT])
        else:
            print ("it already had the suggested mute state" + " " + str(register_02) )



    def set_frequency(self, frequency_kHz):
        #
        # Frequency for calculation has to by in hz and diveded by the frquency of the ocillator of the modul 8192
        
        #allowed frequency have to by between 76 - 108.0 MHz
        if (frequency_kHz < 76000 or frequency_kHz > 108000):
            raise TunerError('Frequency Out of Range')
            
        #save the new frequency
        self._frequency_kHz = frequency_kHz
        
        freq = frequency_kHz * 1000 >> 13
        
        #calculate the two bytes
        lowbyte = freq & 0xff
        highbyte = freq >> 8 & 0xff
        
        self.set_mute(True)
        
        #write the frequency to modul
        self.i2c_write(0x0A , [lowbyte])
        self.i2c_write(0x0B , [highbyte])
        
        #FIXME:
        #write p2, see table in the datasheet "P2 vs. frequency"
        #self.i2c_write(0x07,  [self._p2])
        self.i2c_write(0x07,  [0x7E])
        self.i2c_write(0x07,  [0x0E])
        
        sleep(1)
        #FIXME: here is still the part missing witch setzts MAA Register 
        #print(self.i2c_read_register(0x70))
        #print(R_CEX)
        
        
        self.set_mute(False)
        
    def set_transmit_power(self, rf_power):
        
        register_02 = self.i2c_read_register(0x02)

        if (rf_power == 0):
            register_02 = register_02 & ~RF_POWER_BIT_0
            register_02 = register_02 & ~RF_POWER_BIT_1
            print ("power level 0" + " " + str(register_02))
        elif(rf_power == 1):
            register_02 = register_02 | RF_POWER_BIT_0
            register_02 = register_02 & ~RF_POWER_BIT_1
            print ("power level 1" + " " + str(register_02))     
        elif(rf_power == 2):
            register_02 = register_02 & ~RF_POWER_BIT_0
            register_02 = register_02 | RF_POWER_BIT_1
            print ("power level 2" + " " + str(register_02))      
        elif(rf_power == 3):
            register_02 = register_02 | RF_POWER_BIT_0
            register_02 = register_02 | RF_POWER_BIT_1
            print ("power level 3" + " " + str(register_02))
        else:
            raise TunerError('No valid Option')
        self.i2c_write(0x02, [register_02])

    def set_mode(self, transmitmode):
        pass

