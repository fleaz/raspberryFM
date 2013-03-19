class ns741:
    import smbus
    from time import sleep
    
    def __init__(self, i2cbus,  address, frequency):

        self._address = address
        self._frequency_kHz = frequency
        self._bus = smbus.SMBus(i2cbus)
        self._transmit_power=1
        

    def set_frequency_kHz(self, frequency_kHz):
        #
        #
        freq = frequency_kHz * 1000 >> 13
        
        lowbyte = freq & 0xff
        highbyte = freq >> 8 & 0xff
        self.bus.write_i2c_block_data(self._address, 0x0A , [lowbyte])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x0B , [highbyte])
        sleep(0.01)        
        

    def switch_rf_active(self, state):
        self.bus.write_i2c_block_data(self._address, 0x00 , [0x03])
        sleep(0.01)
    def set_transmit_power(self, power):
        pass
    def set_mode(self, type):
        pass
    def initialize(self):
        init_data = [0x02, 0x83, 0x0A, 0x00,
                     0x00, 0x00, 0x00, 0x7E,
                     0x0E, 0x08, 0x3F, 0x2A,
                     0x0C, 0xE6, 0x3F, 0x70,
                     0x0A, 0xE4, 0x00, 0x42,
                     0xC0, 0x41, 0xF4]
                     
        # intialization data for register 0x00:0x16 */

        iter_reg = 0

        for val in init_data:
            print (str(iter_reg) + ":" + str(val))
            self.bus.write_i2c_block_data(self._address, iter_reg, [val])
            sleep(0.01)

            iter_reg = iter_reg + 1
    
        # TWI_send(0x02, 0x0b);
        # TWI_send(0x15, 0x11);
        # TWI_send(0x10, 0xE0);

        bus.write_i2c_block_data(self._address, 0x02 , [0x0b])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x15 , [0x11])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x10 , [0xE0])
        sleep(0.01)

        # // Configuration
        # TWI_send(0x02, 0x0B);
        # TWI_send(0x07, 0x7E);
        # TWI_send(0x08, 0x0E);
        # TWI_send(0x02, 0xCA); //0x0A Sendeleistung
        # TWI_send(0x01, 0x81);

        self.bus.write_i2c_block_data(self._address, 0x02 , [0x0B])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x07 , [0x7E])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x08 , [0x0E])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x02 , [0x0A])
        sleep(0.01)
        self.bus.write_i2c_block_data(self._address, 0x01 , [0x81])
        sleep(0.01)

