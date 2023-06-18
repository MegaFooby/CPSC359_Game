#Help with setting up the ADXL345
#https://gist.github/xrl/9837382

import smbus, time

bus = smbus.SMBus()
addr = 0x53
bus.open(1)
bus.write_byte_data(addr, 0x31, 0x01)#set a range of +-4g
bus.write_byte_data(addr, 0x2e, 0x00)#create no interrupts
bus.write_byte_data(addr, 0x25, 0x0f)#set the thresh inact register to a higher number
bus.write_byte_data(addr, 0x26, 0)#don't go inactive if left alone for too long
bus.write_byte_data(addr, 0x2d, 0x08)#set to measurement mode
bus.close()

def combinebyte(part1, part0):
    part1 = part1 << 8
    part1 = part1 + part0
    return sxt(part1, 16)

def sxt(number, bits):
    sign = 1 << (bits - 1)
    return (number & (sign - 1)) - (number & sign)

def getx():
    bus.open(1)
    val = bus.read_i2c_block_data(addr, 0x32, 2)
    bus.close()
    return combinebyte(val[1], val[0])

def gety():
    bus.open(1)
    val = bus.read_i2c_block_data(addr, 0x34, 2)
    bus.close()
    return combinebyte(val[1], val[0])

def getz():
    bus.open(1)
    val = bus.read_i2c_block_data(addr, 0x36, 2)
    bus.close()
    return combinebyte(val[1], val[0])

if __name__ == "__main__":
    while True:
        print(getx(), gety(), getz())
        time.sleep(1)