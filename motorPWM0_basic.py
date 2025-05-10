import time
import board
import busio
import pwmio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialize I2C for PCA9685
i2c = busio.I2C(board.GP1, board.GP0)  
pca = PCA9685(i2c)
pca.frequency = 50  # Set PWM frequency for servos (50Hz)

# Create a servo object on channel 0
servo0 = servo.Servo(pca.channels[0])

# Function to move the servo to a specific angle
def move_servo(angle):
    if 0 <= angle <= 180:
        servo0.angle = angle
        print(f"Servo moved to {angle}°")
    else:
        print("Invalid angle! Use 0 to 180.")

# Move servo back and forth
while True:
    for angle in range(0, 181, 10):  # Sweep from 0 to 180 degrees
        move_servo(angle)
        time.sleep(0.1)
    for angle in range(180, -1, -10):  # Sweep back from 180 to 0 degrees
        move_servo(angle)
        time.sleep(0.1)
