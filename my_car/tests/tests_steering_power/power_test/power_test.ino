#include <Servo.h>

// --- Konfiguration ---
// Motor-PWM-Signal (weißer Draht) wird an Pin 14 angeschlossen.
const int motorPin = 14;     
Servo motorController;

// Pulsweiten in Mikrosekunden für den Motor (ESC/Regler)
// Standardwerte (bei ESCs ist 1500 µs in der Regel Neutral/Brake):
const int neutralPulse    = 1500;  // Neutral/Bremsen
const int lowForwardPulse = 1700;  // Niedriger Vorwärtsgang (nicht volle Geschwindigkeit)
const int lowReversePulse = 1300;  // Niedriger Rückwärtsgang

const int step     = 10;      // Schrittweite (in µs)
const int delayMs  = 50;      // Wartezeit zwischen Schritten (50 ms)

void setup() {
  Serial.begin(115200);
  // Initialisiere den Motorcontroller auf dem definierten Pin.
  motorController.attach(motorPin);
  
  // Hinweis:
  // Der Motor wird über eine externe Batterie versorgt!
  // Verbinde den roten Draht der Batterie mit dem roten Anschluss des ESC/Motors
  // und den schwarzen Draht mit dem schwarzen Anschluss.
  // Der GND der Batterie muss mit dem GND des Pico verbunden sein.
}

void loop() {
  // Starte in Neutralstellung
  motorController.writeMicroseconds(neutralPulse);
  Serial.println("Motor in Neutralstellung");
  delay(1000);
  
  // Phase 1: Erhöhe von Neutral (1500 µs) zu niedrigem Vorwärtsgang (1700 µs)
  Serial.println("Niedriger Vorwärtsgang");
  for (int pulse = neutralPulse; pulse <= lowForwardPulse; pulse += step) {
    motorController.writeMicroseconds(pulse);
    Serial.print("PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayMs);
  }
  
  // Zurück zur Neutralstellung
  for (int pulse = lowForwardPulse; pulse >= neutralPulse; pulse -= step) {
    motorController.writeMicroseconds(pulse);
    Serial.print("PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayMs);
  }
  
  delay(1000);
  
  // Phase 2: Reduziere von Neutral (1500 µs) zu niedrigem Rückwärtsgang (1300 µs)
  Serial.println("Niedriger Rückwärtsgang");
  for (int pulse = neutralPulse; pulse >= lowReversePulse; pulse -= step) {
    motorController.writeMicroseconds(pulse);
    Serial.print("PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayMs);
  }
  
  // Zurück zur Neutralstellung
  for (int pulse = lowReversePulse; pulse <= neutralPulse; pulse += step) {
    motorController.writeMicroseconds(pulse);
    Serial.print("PWM-Puls: ");
    Serial.print(pulse);
    Serial.println(" µs");
    delay(delayMs);
  }
  
  delay(1000);
}
