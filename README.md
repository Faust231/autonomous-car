# autonomous-car

A self driving rc car that implements a Raspberry Pi Zero W

1. Raspberry pi imager runterladen

2. config ändern und ssh einrichten

3. 4h lang bgufixen, damit man sich wirklich per ssh hinverbinden kann

- lessons learned:
  - passwort aufschreiben
  - usernamen aufschreiben
  - ssh enablen
  - richtiges netzwerk passwort verwenden und im selben netzwerk sein

4. PWM Signale der Servos herausfinden, indem wir einen Raspberry pi pico mit dem main.py testscript mit den servos verbunden haben

- Lenken:

  - links: 2 ms
  - neutral: 1.5 ms
  - rechts: 1.0 ms

- Fahren:
  - vorwärts: 2 ms
  - neutral/bremsen: 1.5 ms
  - rückwärts: 1 ms

### Ausführen mittels einem Environment:

1. `python3 -m venv car_project_env`

2. `source car_project_env/bin/activate`

3. `pip install opencv-python flask pigpio pyserial`
