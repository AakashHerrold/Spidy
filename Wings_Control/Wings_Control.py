from machine import Pin, I2C
import time

# === I2C Setup ===
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100_000)
pwm = PCA9685(i2c)

# Moves a servo by sending a pulse to the given channel.
# The input is a pulse width in microseconds (e.g. 1500),
# which sets the servo speed using the PCA9685.
def motor_speed(ch, pulse_in_microseconds):
    pulse = int(pulse_in_microseconds * 4096 / 20000)
    pwm.set_pwm(ch, 0, pulse)


# === IHSAN ===
# === Wing Servo Channels ===
WING_SERVO_CHANNEL_LEFT = 10
WING_SERVO_CHANNEL_RIGHT = 11

# === Wing Pulse Values ===
WING_OPEN_PULSE = 1700   
WING_CLOSE_PULSE = 1500  

# === Wing Actions ===
def wing_open():
    print("Wings opening...")
    motor_speed(WING_SERVO_CHANNEL_LEFT, WING_OPEN_PULSE)
    motor_speed(WING_SERVO_CHANNEL_RIGHT, WING_OPEN_PULSE)
    time.sleep(0.3)

def wing_close():
    print("Wings closing...")
    motor_speed(WING_SERVO_CHANNEL_LEFT, WING_CLOSE_PULSE)
    motor_speed(WING_SERVO_CHANNEL_RIGHT, WING_CLOSE_PULSE)
    time.sleep(0.3)


while True:
    wing_open()
    move_forward()
    wing_close()
