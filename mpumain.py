from smbus2 import SMBus
import time
import math
from mpu import init_mpu6050, get_mpu6050_data
import smbus2

def calculate_tilt_angles(accel_data):
    x, y, z = accel_data['x'], accel_data['y'], accel_data['z']

    tilt_x = math.atan2(y, math.sqrt(x * x + z * z)) * 180 / math.pi
    tilt_y = math.atan2(-x, math.sqrt(y * y + z * z)) * 180 / math.pi
    tilt_z = math.atan2(z, math.sqrt(x * x + y * y)) * 180 / math.pi

    return tilt_x, tilt_y, tilt_z

def complimentary_filter(pitch, roll, gyro_data, dt, alpha=0.98):
    pitch += gyro_data['x'] * dt
    roll -= gyro_data['x'] * dt

# i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=4000000)
i2c = smbus2.SMBus(1)
init_mpu6050(i2c)

roll=0
pitch=0

prev_time = time.tick.ms()

while True:
    data = get_mpu6050_data(i2c)
    curr_time = time.tick.ms()
    dt = (curr_time - prev_time) / 1000

    tilt_x, tilt_y, tilt_z = calculate_tilt_angles(data['accel'])
    pitch, roll = complimentary_filter(pitch, roll, data['gyro'], dt)

    prev_time = curr_time

    print("Tilt angles: X: {:.2f}, Y: {:.2f}, Z: {:.2f} degrees".format(tilt_x, tilt_y, tilt_z))
    print("Pitch: {:.2f}, Roll: {:.2f} degrees".format(pitch, roll))
    print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g".format(data['accel']['x'], data['accel']['y'], data['accel']['z']))
    print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} /s".format(data['gyro']['x'], data['gyro']['y'], data['gyro']['z']))
    time.sleep(1)
