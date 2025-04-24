from machine import Pin, I2C
from bh1750 import BH1750
import time

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
