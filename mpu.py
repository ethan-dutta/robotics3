import imutils
import math
import time
from smbus2 import SMBus

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43


def init_mpu6050(i2c, address=0x68):
    i2c.write_byte_data(address, PWR_MGMT_1, 0)
    time.sleep(0.1)
    i2c.write_byte_data(address, SMPLRT_DIV, 7)
    i2c.write_byte_data(address, CONFIG, 0)
    i2c.write_byte_data(address, GYRO_CONFIG, 0)
    i2c.write_byte_data(address, ACCEL_CONFIG, 0)


def read_raw_data(i2c, addr, address=0x68):
    high = i2c.read_byte_data(address, addr, 1)[0]
    low = i2c.read_byte_data(address, addr + 1, 1)[0]
    value = high << 8 | low
    if value > 32768:
        value = value - 65536
    return value

def get_mpu6050_data(i2c):
    accel_x = read_raw_data(i2c, ACCEL_XOUT_H) / 340.0 + 36.53
    accel_y = read_raw_data(i2c, ACCEL_XOUT_H + 2) / 340.0 + 36.53
    accel_z = read_raw_data(i2c, ACCEL_XOUT_H + 4) / 340.0 + 36.53
    gyro_x = read_raw_data(i2c, GYRO_XOUT_H) / 340.0 + 36.53
    gyro_y = read_raw_data(i2c, GYRO_XOUT_H + 2) / 340.0 + 36.53
    gyro_z = read_raw_data(i2c, GYRO_XOUT_H + 4) / 340.0 + 36.53

    return {
        'accel' : {
            'x' : accel_x,
            'y' : accel_y,
            'z' : accel_z,
        },

        'gyro' : {
            'x' : gyro_x,
            'y' : gyro_y,
            'z' : gyro_z,
        }

    }
