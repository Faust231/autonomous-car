#include <Servo.h>

// Servo-Objekte für Motor (ESC) und Lenkung
Servo motorServo;
Servo steeringServo;

const int onboardLED = 25;    // Onboard-LED (GPIO25 beim Pico)

// --- PWM-Pulsweiten in Mikrosekunden ---

// Für den Motor (VXL‑3S ESC)
// Standardwerte: 1000 µs = Rückwärts, 1500 µs = Neutral/Bremsen, 2000 µs = Vorwärts
const int motor_minPulse = 1200;  
const int motor_midPulse = 1500;  
const int motor_maxPulse = 1700;  

// Für die Lenkung (Standard-Servo)
// 1000 µs = volle linke Stellung, 1500 µs = Zentrum, 2000 µs = volle rechte Stellung
const int steering_leftPulse   = 1000;
const int steering_centerPulse = 1500;
const int steering_rightPulse  = 2000;

// Schrittweite und Verzögerung für den Sweep (in µs bzw. Millisekunden)
const int step = 10;      // Schrittweite in µs
const int delayTime = 50; // Verzögerung zwischen den Schritten in Millisekunden

void setup() {
  Serial.begin(115200);
  
  // Servo-Objekte an die gewünschten Pins anhängen
  motorServo.attach(14);
  steeringServo.attach(15);
  
  Serial.println("Test von Motor (Port 14) und Lenkung (Port 15) gestartet.");
}

void loop() {
  // ======================
  // Motor-Test (Port 14)
  // ======================
  Serial.println("\n--- MOTOR-TEST ---");
  // Setze Motor auf Neutral (1500 µs)
  motorServo.writeMicroseconds(motor_midPulse);
  Serial.println("Motor: Neutral (1500 µs)");
  delay(500);
  
  // Vorwärts: von Neutral (1500) zu Vorwärts (2000 µs)
  Serial.println("Motor: Vorwärts (1500 -> 2000 µs)");
  for (int pulse = motor_midPulse; pulse <= motor_maxPulse; pulse += step) {
    motorServo.writeMicroseconds(pulse);
    Serial.print("Motor PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  // Zurück zu Neutral
  Serial.println("Motor: Zurück zu Neutral (2000 -> 1500 µs)");
  for (int pulse = motor_maxPulse; pulse >= motor_midPulse; pulse -= step) {
    motorServo.writeMicroseconds(pulse);
    Serial.print("Motor PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  delay(500);
  
  // Rückwärts: von Neutral (1500) zu Rückwärts (1000 µs)
  Serial.println("Motor: Rückwärts (1500 -> 1000 µs)");
  for (int pulse = motor_midPulse; pulse >= motor_minPulse; pulse -= step) {
    motorServo.writeMicroseconds(pulse);
    Serial.print("Motor PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  // Zurück zu Neutral
  Serial.println("Motor: Zurück zu Neutral (1000 -> 1500 µs)");
  for (int pulse = motor_minPulse; pulse <= motor_midPulse; pulse += step) {
    motorServo.writeMicroseconds(pulse);
    Serial.print("Motor PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  delay(500);
  
  // ======================
  // Lenkungs-Test (Port 15)
  // ======================
  Serial.println("\n--- LENKUNGS-TEST ---");
  // Setze Lenkung auf Zentrum (1500 µs)
  steeringServo.writeMicroseconds(steering_centerPulse);
  Serial.println("Lenkung: Zentrum (1500 µs)");
  delay(500);
  
  // Links: von Zentrum (1500) zu voller Linksdrehung (1000 µs)
  Serial.println("Lenkung: Links (1500 -> 1000 µs)");
  for (int pulse = steering_centerPulse; pulse >= steering_leftPulse; pulse -= step) {
    steeringServo.writeMicroseconds(pulse);
    Serial.print("Lenkung PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  // Zurück zur Zentrierung von links
  Serial.println("Lenkung: Zurück zur Zentrierung (1000 -> 1500 µs)");
  for (int pulse = steering_leftPulse; pulse <= steering_centerPulse; pulse += step) {
    steeringServo.writeMicroseconds(pulse);
    Serial.print("Lenkung PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  // Rechts: von Zentrum (1500) zu voller Rechtsdrehung (2000 µs)
  Serial.println("Lenkung: Rechts (1500 -> 2000 µs)");
  for (int pulse = steering_centerPulse; pulse <= steering_rightPulse; pulse += step) {
    steeringServo.writeMicroseconds(pulse);
    Serial.print("Lenkung PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  // Zurück zur Zentrierung von rechts
  Serial.println("Lenkung: Zurück zur Zentrierung (2000 -> 1500 µs)");
  for (int pulse = steering_rightPulse; pulse >= steering_centerPulse; pulse -= step) {
    steeringServo.writeMicroseconds(pulse);
    Serial.print("Lenkung PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayTime);
  }
  
  delay(1000); // Pause, bevor der Zyklus von vorne beginnt
}
