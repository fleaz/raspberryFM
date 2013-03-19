class ns741:
    import smbus
    from time import sleep
    bus = smbus.SMBus(0)

    
    def __init__(self, address, frequency):

        self.address = address
        self.frequency_kHz = frequency

        # intialization data for register 0x00:0x16 */

        init_data = [0x02, 0x83, 0x0A, 0x00,
                     0x00, 0x00, 0x00, 0x7E,
                     0x0E, 0x08, 0x3F, 0x2A,
                     0x0C, 0xE6, 0x3F, 0x70,
                     0x0A, 0xE4, 0x00, 0x42,
                     0xC0, 0x41, 0xF4]

        iter_reg = 0

        for val in init_data:
            print (str(iter_reg) + ":" + str(val))
            bus.write_i2c_block_data(_address, iter_reg, [val])
            sleep(0.01)

            iter_reg = iter_reg + 1
    
        #	TWI_send(0x02, 0x0b);
        #	TWI_send(0x15, 0x11);
        #	TWI_send(0x10, 0xE0);

        bus.write_i2c_block_data(_address, 0x02 , [0x0b])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x15 , [0x11])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x10 , [0xE0])
        sleep(0.01)

        #	// Configuration
        #	TWI_send(0x02, 0x0B);
        #	TWI_send(0x07, 0x7E);
        #	TWI_send(0x08, 0x0E);
        #	TWI_send(0x02, 0xCA);	//0x0A Sendeleistung
        #	TWI_send(0x01, 0x81);

        bus.write_i2c_block_data(_address, 0x02 , [0x0B])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x07 , [0x7E])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x08 , [0x0E])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x02 , [0x0A])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x01 , [0x81])
        sleep(0.01)

        bus.write_i2c_block_data(_address, 0x0A , [0xA3])
        sleep(0.01)
        bus.write_i2c_block_data(_address, 0x0B , [0x30])
        sleep(0.01)

        bus.write_i2c_block_data(_address, 0x00 , [0x03])
        sleep(0.01)

    def set_frequency_kHz(self, frequency_kHz):
        pass
    def switch_rf_active(self, state):
        pass
    def set_transmit_power(self, power):
        pass
    def set_mode(self, type):
        pass
    
    def initialize(self):
        pass
