from smbus2 import Pin, I2C
import time
from pca9685 import PCA9685  # Make sure you have a PCA9685 library

# Initialize I2C
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)  # SCL=GP5, SDA=GP4

# Initialize PCA9685
pwm = PCA9685(i2c)
pwm.freq(50)  # Set PWM frequency (for servos, 50Hz is common)

# Function to set servo angle
def set_servo_angle(channel, angle):
    min_pulse = 150  # Minimum pulse length
    max_pulse = 600  # Maximum pulse length
    pulse = int(min_pulse + (angle / 180) * (max_pulse - min_pulse))
    pwm.duty(channel, pulse)

# Example: Move servo on channel 0
while True:
    for angle in range(0, 181, 10):  # 0 to 180 degrees
        set_servo_angle(0, angle)
        time.sleep(0.1)
    for angle in range(180, -1, -10):  # 180 to 0 degrees
        set_servo_angle(0, angle)
        time.sleep(0.1)
