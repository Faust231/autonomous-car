<img src="file:///Users/johnyhamsik12/Downloads/IMG_7295.jpeg" title="" alt="IMG_7295.jpeg" width="188">

Das ist der Controller und Receiver zugleich. Mit dem kann den Motor und die Lenkung ansteuern. Bei Chanel 1ganz unten läuft die Lenkung und bei Chanel 2 (Reihenfolge 3) läuft die Steuereinheit wo man dann auch den Motor ansteuern kann.

<img src="file:///Users/johnyhamsik12/Downloads/IMG_7297.jpeg" title="" alt="IMG_7297.jpeg" width="346">

Das ist der Telemetry Sensor welcher uns hilft die Geschwindigkeit und Umdrehungen zu sehen.
Ebenso haben wir eine App wo wir das ganzen Messen und beobachten können namens Trexxes Link.

```bash
import RPi.GPIO as GPIO
import time

# GPIO-Pin für PWM
PWM_PIN = 1
FREQ = 50  # 50 Hz für Steuerungssignal

# PWM-Bereich (Duty Cycle für 1–2 ms Pulsweite)
NEUTRAL = 7.5  # 1,5 ms = Neutral (Bremsen)
FORWARD = 10   # 2 ms = Volle Geschwindigkeit vorwärts
REVERSE = 5    # 1 ms = Volle Geschwindigkeit rückwärts

# GPIO einrichten
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, FREQ)
pwm.start(NEUTRAL)  # Start im Neutralzustand

def set_speed(duty_cycle):
    print(f"Setting duty cycle to {duty_cycle}%")
    pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        cmd = input("Befehl (f = vorwärts, r = rückwärts, b = bremsen, q = quit): ")

        if cmd == 'f':
            set_speed(FORWARD)  # Vorwärts
        elif cmd == 'r':
            set_speed(REVERSE)  # Rückwärts
        elif cmd == 'b':
            set_speed(NEUTRAL)  # Bremsen
        elif cmd == 'q':
            break
        else:
            print("Ungültiger Befehl")

finally:
    pwm.stop()
    GPIO.cleanup()
```

Der Servo Motor hat wahrscheinlich 50 hz zum steuern. Oben im code sind die PWM Einstellungen.

Der Anschluss mit dem Pico und der Steuerung:


![IMG_7360.png](/Users/johnyhamsik12/Downloads/IMG_7360.png)



![IMG_7359.png](/Users/johnyhamsik12/Downloads/IMG_7359.png)



![IMG_7358.png](/Users/johnyhamsik12/Downloads/IMG_7358.png)

Wir haben den Port 15 für den Servo und die Steuerung und den Pin 14 für den Motor.
