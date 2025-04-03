from machine import Pin, PWM
import time

# Setup PWM on pin 15 for servo control at 50 Hz (20 ms period)
pwm1 = PWM(Pin(15))
pwm1.freq(50)

# Setup onboard LED (GPIO25 on the Pico)
led = Pin(25, Pin.OUT)
led.value(1)  # Turn the LED on

def pulse_to_duty(pulse_us):
    # For a 50 Hz signal, the period is 20000 microseconds.
    # Convert a pulse width in microseconds to a duty cycle value (0-65535)
    return int((pulse_us / 20000) * 65535)

# Define pulse width limits in microseconds:
min_pulse = 1000   # 1.0 ms
mid_pulse = 1500   # 1.5 ms (starting point)
max_pulse = 2000   # 2.0 ms

step = 10          # Change pulse width in steps of 10 us
delay = 0.05       # Delay between steps (adjust for speed of change)

while True:
    # Phase 1: Decrease from mid (1.5 ms) to minimum (1.0 ms)
    for pulse in range(mid_pulse, min_pulse - 1, -step):
        duty = pulse_to_duty(pulse)
        pwm1.duty_u16(duty)
        print("Pulse width: {:.1f} ms, Duty: {}".format(pulse/1000, duty))
        time.sleep(delay)
    
    # Phase 2: Increase from minimum (1.0 ms) to maximum (2.0 ms)
    for pulse in range(min_pulse, max_pulse + 1, step):
        duty = pulse_to_duty(pulse)
        pwm1.duty_u16(duty)
        print("Pulse width: {:.1f} ms, Duty: {}".format(pulse/1000, duty))
        time.sleep(delay)
    
    # Phase 3: Decrease from maximum (2.0 ms) back to mid (1.5 ms)
    for pulse in range(max_pulse, mid_pulse - 1, -step):
        duty = pulse_to_duty(pulse)
        pwm1.duty_u16(duty)
        print("Pulse width: {:.1f} ms, Duty: {}".format(pulse/1000, duty))
        time.sleep(delay)
