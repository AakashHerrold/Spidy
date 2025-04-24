from machine import Pin, I2C
from bh1750 import BH1750
import time

# === PETER ===
# === PCA9685 Setup ===
class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()
        self.set_pwm_freq(50)

    def reset(self):
        self.i2c.writeto_mem(self.address, 0x00, b'\x00')

    def set_pwm_freq(self, freq_hz):
        prescale = int(25000000.0 / (4096 * freq_hz) - 1)
        old_mode = self.i2c.readfrom_mem(self.address, 0x00, 1)
        self.i2c.writeto_mem(self.address, 0x00, bytes([old_mode[0] & 0x7F | 0x10]))
        self.i2c.writeto_mem(self.address, 0xFE, bytes([prescale]))
        self.i2c.writeto_mem(self.address, 0x00, old_mode)
        time.sleep_ms(5)
        self.i2c.writeto_mem(self.address, 0x00, bytes([old_mode[0] | 0xA1]))

    def set_pwm(self, ch, on, off):
        reg = 0x06 + 4 * ch
        data = bytearray([on & 0xFF, on >> 8, off & 0xFF, off >> 8])
        self.i2c.writeto_mem(self.address, reg, data)

# === I2C Setup ===
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100_000)
pwm = PCA9685(i2c)

# Moves a servo by sending a pulse to the given channel.
# The input is a pulse width in microseconds (e.g. 1500),
# which sets the servo speed using the PCA9685.
def motor_speed(ch, pulse_in_microseconds):
    pulse = int(pulse_in_microseconds * 4096 / 20000)
    pwm.set_pwm(ch, 0, pulse)

# === PCA9685 Channel Assignments ===
# Left legs 
left_leg1_lift = 0
left_leg2_lift = 1
left_leg1_swing = 4
left_leg2_swing = 5

# Right legs
right_leg1_lift = 2
right_leg2_lift = 3
right_leg1_swing = 6
right_leg2_swing = 7

# === Actions ===
def lift(ch): motor_speed(ch, 1700)
def drop(ch): motor_speed(ch, 1500)
def swing_forward(ch): motor_speed(ch, 1500)
def swing_backwards(ch): motor_speed(ch, 1700)
def stop(ch): motor_speed(ch, 1540)

# Supporting Legs (8 & 9)
motor_speed(8, 1450)
time.sleep(0.2)
motor_speed(8, 1540)

motor_speed(9, 1700)
time.sleep(0.15)
motor_speed(9, 1540)

def move_forward():
    print(" Step 1: Left Leg 1 + Right Leg 2")
    lift(left_leg1_lift)
    lift(right_leg2_lift)
    time.sleep(0.2)

    swing_backwards(left_leg1_swing)
    swing_backwards(right_leg2_swing)
    time.sleep(0.25)

    drop(left_leg1_lift)
    drop(right_leg2_lift)
    time.sleep(0.2)

    stop(left_leg1_lift)
    stop(left_leg1_swing)
    stop(right_leg2_lift)
    stop(right_leg2_swing)
    time.sleep(0.3)

    print(" Step 2: Right Leg 1 + Left Leg 2")
    lift(right_leg1_lift)
    lift(left_leg2_lift)
    time.sleep(0.2)

    swing_backwards(right_leg1_swing)
    swing_backwards(left_leg2_swing)
    time.sleep(0.25)

    drop(right_leg1_lift)
    drop(left_leg2_lift)
    time.sleep(0.2)

    stop(right_leg1_lift)
    stop(right_leg1_swing)
    stop(left_leg2_lift)
    stop(left_leg2_swing)
    time.sleep(0.3)
    
    print(" Step 1: Left Leg 1 + Right Leg 2")
    lift(left_leg1_lift)
    lift(right_leg2_lift)
    time.sleep(0.2)

    swing_forward(left_leg1_swing)
    swing_forward(right_leg2_swing)
    time.sleep(0.50)

    drop(left_leg1_lift)
    drop(right_leg2_lift)
    time.sleep(0.2)

    stop(left_leg1_lift)
    stop(left_leg1_swing)
    stop(right_leg2_lift)
    stop(right_leg2_swing)
    time.sleep(0.3)

    print(" Step 2: Right Leg 1 + Left Leg 2")
    lift(right_leg1_lift)
    lift(left_leg2_lift)
    time.sleep(0.2)

    swing_forward(right_leg1_swing)
    swing_forward(left_leg2_swing)
    time.sleep(0.50)

    drop(right_leg1_lift)
    drop(left_leg2_lift)
    time.sleep(0.2)

    stop(right_leg1_lift)
    stop(right_leg1_swing)
    stop(left_leg2_lift)
    stop(left_leg2_swing)
    time.sleep(0.3)

def move_left():
    print(" Turning left")
    lift(left_leg1_lift)
    lift(right_leg2_lift)
    time.sleep(0.2)

    swing_backwards(left_leg1_swing)
    swing_backwards(right_leg2_swing)
    time.sleep(0.25)

    drop(left_leg1_lift)
    drop(right_leg2_lift)
    time.sleep(0.2)

    stop(left_leg1_lift)
    stop(left_leg1_swing)
    stop(right_leg2_lift)
    stop(right_leg2_swing)
    time.sleep(0.3)

    print(" Step 2: Right Leg 1 + Left Leg 2")
    lift(right_leg1_lift)
    lift(left_leg2_lift)
    time.sleep(0.2)

    swing_backwards(right_leg1_swing)
    swing_backwards(left_leg2_swing)
    time.sleep(0.25)

    drop(right_leg1_lift)
    drop(left_leg2_lift)
    time.sleep(0.2)

    stop(right_leg1_lift)
    stop(right_leg1_swing)
    stop(left_leg2_lift)
    stop(left_leg2_swing)
    time.sleep(0.3)
    
def move_right():
    print(" Turning left")
    lift(left_leg1_lift)
    lift(right_leg2_lift)
    time.sleep(0.2)

    swing_forward(left_leg1_swing)
    swing_forward(right_leg2_swing)
    time.sleep(0.25)

    drop(left_leg1_lift)
    drop(right_leg2_lift)
    time.sleep(0.2)

    stop(left_leg1_lift)
    stop(left_leg1_swing)
    stop(right_leg2_lift)
    stop(right_leg2_swing)
    time.sleep(0.3)

    print(" Step 2: Right Leg 1 + Left Leg 2")
    lift(right_leg1_lift)
    lift(left_leg2_lift)
    time.sleep(0.2)

    swing_forward(right_leg1_swing)
    swing_forward(left_leg2_swing)
    time.sleep(0.25)

    drop(right_leg1_lift)
    drop(left_leg2_lift)
    time.sleep(0.2)

    stop(right_leg1_lift)
    stop(right_leg1_swing)
    stop(left_leg2_lift)
    stop(left_leg2_swing)
    time.sleep(0.3)
#==========================================================
    
# === IHSAN ===
# === Wing Servo Channels ===
WING_SERVO_CHANNEL_LEFT = 10
WING_SERVO_CHANNEL_RIGHT = 11

# === Wing Pulse Values ===
WING_OPEN_PULSE = 1700   
WING_CLOSE_PULSE = 1500  

# === Wing Control Function ===
def control_wings(action):
    if action == "open":
        print("Wings opening...")
        motor_speed(WING_SERVO_CHANNEL_LEFT, WING_OPEN_PULSE)
        motor_speed(WING_SERVO_CHANNEL_RIGHT, WING_OPEN_PULSE)
    elif action == "close":
        print("Wings closing...")
        motor_speed(WING_SERVO_CHANNEL_LEFT, WING_CLOSE_PULSE)
        motor_speed(WING_SERVO_CHANNEL_RIGHT, WING_CLOSE_PULSE)
    else:
        print("Invalid action. Use 'open' or 'close'.")
    time.sleep(0.3)
#==========================================================
#========================== SAM ===========================
#Pin wiring#
TRIG_PIN_1, ECHO_PIN_1 = 6, 7     # Sensor 1  (GP6 / GP7)
TRIG_PIN_2, ECHO_PIN_2 = 10, 11   # Sensor 2  (GP10 / GP11)

#Constants#
CM_PER_US            = 0.0343     # speed of sound, cm per micro‑second
RAPID_CM_PER_SEC     = 100.0      # tweak: what counts as "fast"?
READ_INTERVAL_S      = 0.10       # main‑loop period (10 Hz)

#Pin objects #
Trigger_1 = Pin(TRIG_PIN_1, Pin.OUT)
Echo_1 = Pin(ECHO_PIN_1, Pin.IN)

Triger_2 = Pin(TRIG_PIN_2, Pin.OUT)
Echo_2 = Pin(ECHO_PIN_2, Pin.IN)

#State for speed calc#
Previous_time   = None   # timestamp of previous loop
Previous_distance_1  = None   # previous distance from sensor 1
Previous_distance_2  = None   # previous distance from sensor 2


#low‑level distance helper#
def get_distance(trig_pin: Pin, echo_pin: Pin) -> float:

    trig_pin.value(0)
    utime.sleep_us(2)

    trig_pin.value(1)
    utime.sleep_us(10)
    trig_pin.value(0)

    # wait for echo HIGH to start
    start = utime.ticks_us()
    while echo_pin.value() == 0:
        start = utime.ticks_us()

    # wait for echo LOW to stop
    stop = start
    while echo_pin.value() == 1:
        stop = utime.ticks_us()

    pulse = utime.ticks_diff(stop, start)          # round‑trip µs
    return (pulse * CM_PER_US) / 2                 # one‑way cm

#====================== AIMAN ============================
# from machine import Pin, SoftI2C
# from bh1750 import BH1750
# import time
# 
# i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=400000)
# 
# sensor = BH1750(bus=i2c, addr=0x23)
# 
# try:
#     while True:
#         lux = sensor.luminance(BH1750.CONT_HIRES_1)
#         print("Luminance: {:.2f} lux".format(lux))
#         time.sleep(2)
# 
# except Exception as e:
#     print("Error:", e)
#==========================================================

#==================== AAKASH HERROLD / AIMAN ======================
# Initialising I2C communication
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# Creating BH1750 object
light_sensor = BH1750(bus=i2c, addr=0x23)

def stop_all_motors():
    for ch in range(12):
        stop(ch)

def analyze_environment(light_sensor, sample_count=20, delay=0.2, dark_threshold=20, stability_margin=100):
    readings = []
    
    for _ in range(sample_count):
        lux = light_sensor.luminance(BH1750.CONT_HIRES_1)
        readings.append(lux)
        time.sleep(delay)

    avg_lux = sum(readings) / len(readings)
    lux_range = max(readings) - min(readings)

    brightness = 'bright' if avg_lux > dark_threshold else 'dark'
    stability = 'unstable' if lux_range > stability_margin else 'stable'

    print("\n[Environment Analysis]")
    print("Readings:", ["{:.2f}".format(r) for r in readings])
    print("Average Lux: {:.2f}", avg_lux)
    print("Range:", lux_range)
    print("Brightness:", brightness)
    print("Stability:", stability)
    print("------------------------")

    return brightness, stability
    
    
brightness, stability = analyze_environment(light_sensor)

condition = 0
if brightness == 'bright' and stability == 'stable':
    print("Bright and steady environment. Good to go.")
    condition = 1
    
elif brightness == 'dark' and stability == 'unstable':
    print("Caution: Flickering dark environment. Adjusting behavior.")
    condition = 0
#==========================================================
while True:
    
#==================== SAM ======================
    # Fresh measurements
    dist1_cm = get_distance(Trigger_1, Echo_1)
    dist2_cm = get_distance(Triger_2, Echo_2)

    # Work out speeds since last reading
    now_ms = utime.ticks_ms()
    rapid1 = rapid2 = False

    if Previous_time is not None:  # Skip first iteration
        dt_s = utime.ticks_diff(now_ms, Previous_time) / 1000.0
        if dt_s > 0:
            speed1 = abs(dist1_cm - Previous_distance_1) / dt_s  
            speed2 = abs(dist2_cm - Previous_distance_2) / dt_s
            rapid1 = speed1 > RAPID_CM_PER_SEC
            rapid2 = speed2 > RAPID_CM_PER_SEC

    # Remember values for next iteration
    Previous_time = now_ms
    Previous_distance_1 = dist1_cm
    Previous_distance_2 = dist2_cm
    
    # ============= AAKASH HERROLD ===============
    if (dist1_cm <= 15 and dist2_cm >= 15):
        move_right()
    if (dist1_cm >= 15 and dist2_cm <= 15):
        move_left()
    if (dist1_cm <= 15 and dist2_cm <= 15):
        move_right()
    #============================================
    

    # Output based on readings
    if rapid1 and rapid2:
        print(f"Sensor 1: {dist1_cm:6.2f} cm – Object approaching rapidly!")
        print(f"Sensor 2: {dist2_cm:6.2f} cm – Object approaching rapidly!")
        stop_all_motors()
        action = "open"
        control_wings()
    elif rapid1:
        print(f"Sensor 1: {dist1_cm:6.2f} cm – Object approaching rapidly!")
        print(f"Sensor 2: {dist2_cm:6.2f} cm")
        
    elif rapid2:
        print(f"Sensor 1: {dist1_cm:6.2f} cm")
        print(f"Sensor 2: {dist2_cm:6.2f} cm – Object approaching rapidly!")
    else:
        print(f"Sensor 1: {dist1_cm:6.2f} cm")
        print(f"Sensor 2: {dist2_cm:6.2f} cm")
        action = "close"
        control_wings()

    utime.sleep(READ_INTERVAL_S)
    
#==========================================================
#==================== AAKASH HERROLD ======================
    
      if condition == 1:
          
        lux = light_sensor.luminance(BH1750.CONT_HIRES_1)
        print("Luminance: {:.2f} lux".format(lux))
        if lux > 600:
                print("Too bright – stopping.")
                stop_all_motors()
                
        elif 450 < lux <= 600:
            print("Very close to light – slowing down.")
            move_forward()

        elif 150 < lux <= 450:
            print("Medium range – approach light.")
            move_forward()

        elif 50 < lux <= 150:
            print("Far from light – move quickly.")
            move_forward()

        else:
            print("Room light – searching for brighter area.")
            move_forward()
    
      else:
          brightness, stability = analyze_environment(light_sensor)
          if brightness == 'bright' and stability == 'stable':
            print("Bright and steady environment. Good to go.")
            condition = 1
                
          elif brightness == 'dark' and stability == 'unstable':
            print("Caution: Flickering dark environment. Adjusting behavior.")
            condition = 0

#==========================================================
