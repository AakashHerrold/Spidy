from machine import Pin
import utime

#Pin wiring#
TRIG_PIN_1, ECHO_PIN_1 = 6, 7     # Sensor 1  (GP6 / GP7)
TRIG_PIN_2, ECHO_PIN_2 = 10, 11   # Sensor 2  (GP10 / GP11)

#Constants#
CM_PER_US            = 0.0343     # speed of sound, cm per micro‑second
RAPID_CM_PER_SEC     = 100.0      # tweak: what counts as "fast"?
READ_INTERVAL_S      = 0.10       # main‑loop period (10 Hz)

#Pin objects #
Trigger_1 = Pin(TRIG_PIN_1, Pin.OUT)
Echo_1 = Pin(ECHO_PIN_1, Pin.IN)

Triger_2 = Pin(TRIG_PIN_2, Pin.OUT)
Echo_2 = Pin(ECHO_PIN_2, Pin.IN)

#State for speed calc#
Previous_time   = None   # timestamp of previous loop
Previous_distance_1  = None   # previous distance from sensor 1
Previous_distance_2  = None   # previous distance from sensor 2


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


#main loop #
print("Continuous read‑out \n")
while True:
    #fresh measurements
    dist1_cm = get_distance(Trigger_1, Echo_1)
    dist2_cm = get_distance(Triger_2, Echo_2)

    #work out speeds since last reading 
    now_ms = utime.ticks_ms()
    rapid1 = rapid2 = False

    if Previous_time is not None:                   # skip first iteration
        dt_s = utime.ticks_diff(now_ms, Previous_time) / 1000.0
        if dt_s > 0:
            speed1 = abs(dist1_cm - Previous_distance_1) / dt_s  
            speed2 = abs(dist2_cm - Previous_distance_2) / dt_s
            rapid1 = speed1 > RAPID_CM_PER_SEC
            rapid2 = speed2 > RAPID_CM_PER_SEC

    #remember for next time
    Previous_time  = now_ms
    Previous_distance_1 = dist1_cm
    Previous_distance_2 = dist2_cm

    # --- nice print‑out ---
    tag1 = "Object coming" if rapid1 else ""
    tag2 = "Ojbect coming" if rapid2 else ""
    print(f"Sensor 1: {dist1_cm:6.2f} cm{tag1}   |   Sensor 2: {dist2_cm:6.2f} cm{tag2}")

    utime.sleep(READ_INTERVAL_S)
