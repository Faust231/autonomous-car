#include <Servo.h>

// Pin-Zuweisungen (anpassen, falls nötig)
const int servoPin = 15;      // PWM-Ausgang für den Servo
const int onboardLED = 25;    // Onboard-LED (GPIO25 beim Pico)

// Pulsweiten in Mikrosekunden
const int minPulse = 1000;    // 1,0 ms
const int midPulse = 1500;    // 1,5 ms (Start-/Neutralposition)
const int maxPulse = 2000;    // 2,0 ms

const int step = 10;          // Änderung in 10 µs-Schritten
const int delayMs = 50;       // Wartezeit zwischen den Schritten (50 ms)

Servo myServo;

void setup() {
  // Serielle Kommunikation zur Ausgabe der Pulsweiten
  Serial.begin(115200);
  
  // Servo am definierten Pin anschließen
  myServo.attach(servoPin);
  
  // Onboard-LED als Ausgang konfigurieren und einschalten
  pinMode(onboardLED, OUTPUT);
  digitalWrite(onboardLED, HIGH);
}

void loop() {
  // Phase 1: Von der mittleren Position (1,5 ms) zur minimalen Position (1,0 ms) abwärts
  for (int pulse = midPulse; pulse >= minPulse; pulse -= step) {
    myServo.writeMicroseconds(pulse);
    Serial.print("Pulse width: ");
    Serial.print(pulse / 1000.0, 1);
    Serial.println(" ms");
    delay(delayMs);
  }
  
  // Phase 2: Von minimal (1,0 ms) zu maximal (2,0 ms) aufwärts
  for (int pulse = minPulse; pulse <= maxPulse; pulse += step) {
    myServo.writeMicroseconds(pulse);
    Serial.print("Pulse width: ");
    Serial.print(pulse / 1000.0, 1);
    Serial.println(" ms");
    delay(delayMs);
  }
  
  // Phase 3: Von maximal (2,0 ms) zurück zur mittleren Position (1,5 ms) abwärts
  for (int pulse = maxPulse; pulse >= midPulse; pulse -= step) {
    myServo.writeMicroseconds(pulse);
    Serial.print("Pulse width: ");
    Serial.print(pulse / 1000.0, 1);
    Serial.println(" ms");
    delay(delayMs);
  }
}
