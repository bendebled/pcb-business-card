"""
This is a MicroPython driver for the Dallas (Maxim) DS1621 digital temperature sensor.

The DS1621 is an I2C device, and is able to provide digital temperature data with a resolution of 9 bits, resulting in a
granularity of 0.5 degrees Celsius.

Additionally, the DS1621 is a relatively simple device; as such, the I2C command set is rather simple. The simplicity is
a great factor for utilizing this device (and driver) as a simple example for use of I2C on MicroPython; the basic read,
write, and other functionality are demonstrated. Additionally, some simple data manipulation methods are demonstrated.
"""
import machine
import utime
import ustruct
from micropython import const


# Define the base DS1621 I2C device address (ie: A0 == 0, A1 == 0, A2 == 0)
DS1621_I2C_ADDRESS_MINIMUM = const(0x48)
DS1621_I2C_ADDRESS_MAXIMUM = const(0x4F)


# Define parameters related to the temperature data register.
# The high and low temperature registers are combined to create a 9-bit "two's complement" signed integer value, which
# represents the temperature in increments of 0.5 degrees Celsius. Data is written MSB-first.
DS1621_REG_FORMAT = '>h'
DS1621_REG_SHIFT = 7


# Define DS1621 commands
DS1621_CMD_READ_TEMP = const(0xAA)
DS1621_CMD_ACCESS_TH = const(0xA1)
DS1621_CMD_ACCESS_TL = const(0xA2)
DS1621_CMD_START_CONV = const(0xEE)
DS1621_CMD_STOP_CONV = const(0x22)
DS1621_CMD_ACCESS_CFG = const(0xAC)


class DS1621:
    """
    Class for communicating with the DS1621 I2C digital temperature sensor.
    """

    def __init__(self, device_address=DS1621_I2C_ADDRESS_MINIMUM, i2c=None):
        """
        Initialize the object for utilizing the DS1621 temperature sensor.

        :param device_address: The device's I2C address, as set by the A0, A1, and A2 pins on the device.
                               Valid values are 0x48 (A[0-2] == 0) to 0x4F (A[0-2] == 1). The default value is 0x48.
        :param i2c: The I2C object through which communication with the DS1621 will occur. If not specified, an error
                    will result.
        """

        # Ensure we have a valid I2C object
        if i2c is None:
            raise ValueError('An I2C object is required.')

        # Ensure the device address is within the valid range
        if (device_address < DS1621_I2C_ADDRESS_MINIMUM) or (device_address > DS1621_I2C_ADDRESS_MAXIMUM):
            raise ValueError('The device I2C address is out of bounds.')

        self._i2c = i2c
        self._devaddr = device_address
        self._temp = bytearray(1)


    def write_cmd(self, cmd):
        self._temp[0] = cmd
        self._i2c.writeto(self._devaddr, self._temp)


    def read_temperature(self, register=DS1621_CMD_READ_TEMP):
        self._temp[0] = register
        self._i2c.writeto(self._devaddr, self._temp, False)
        data = self._i2c.readfrom(self._devaddr, 2)
        value = ustruct.unpack(DS1621_REG_FORMAT, data)[0] >> DS1621_REG_SHIFT
        return value


    def start_conversion(self):
        self.write_cmd(DS1621_CMD_START_CONV)


    def stop_conversion(self):
        self.write_cmd(DS1621_CMD_STOP_CONV)


    def read_access_config(self):
        self._temp[0] = DS1621_CMD_ACCESS_CFG
        self._i2c.writeto(self._devaddr, self._temp, False)
        return self._i2c.readfrom(self._devaddr, 1)


    def write_access_config(self, value):
        written = self._i2c.writeto(self._devaddr, DS1621_CMD_ACCESS_TH + ustruct.pack('b', value))
        assert written == 2, "Access Config write returned: %d ?" % written


    def display_continuous(self):
        self.start_conversion()
        try:
            while True:
                print('Temp: %.3fF' % (self.read_temperature() * 9 / 10 + 32))
                utime.sleep(2)
        except:
            self.stop_conversion()
            raise


    def print_temperature_data(self):
        # Ensure the I2C device is present
        devices = self._i2c.scan()
        assert (self._devaddr in devices,
                "DS1621 with address %d was not present in scan results:\n%s" % self._devaddr, devices)
        self.display_continuous()

