import lgpio
from time import sleep

GPIO_CHIP = 0
SERVO_GPIO = 17  # Use GPIO 18 (physical pin 12), known for better PWM support
h = lgpio.gpiochip_open(GPIO_CHIP)

# Helper function to send servo pulse (in ms)
def send_servo_pulse(pulse_ms):
    """
    Sends a pulse with a duration of pulse_ms (1.0 to 2.0 ms)
    at approximately 50 Hz typical for a servo.
    """
    period_ms = 20  # 20ms period = 50Hz for servo
    pulse_us = int(pulse_ms * 10)  # Convert to microseconds
    rest_us = (period_ms * 10) - pulse_us  # Time for LOW pulse

    # Write HIGH for pulse duration
    lgpio.gpio_write(h, SERVO_GPIO, 1)
    # lgpio.time_sleep(pulse_us / 1e3)
    sleep(pulse_us/1e3)
    # Write LOW for the rest of the period
    lgpio.gpio_write(h, SERVO_GPIO, 0)
    sleep(pulse_us/1e3)

# Helper function to move the servo to a specific angle
def set_angle(angle):
    # Limit the angle to valid servo range: 0 to 180 degrees
    angle = max(0, min(180, angle))
    
    # Convert angle to pulse duration (1.0 ms to 2.0 ms)
    pulse_ms = 1.0 + (angle / 180.0) * 1.0  # Mapping 0-180ï¿½ to 1.0-2.0 ms
    send_servo_pulse(pulse_ms)

try:
    # Set the pin as an output pin
    lgpio.gpio_claim_output(h, SERVO_GPIO)

    # Move servo to 0ï¿½ (1.0 ms pulse)
    print("Moving to 0ï¿½")
    set_angle(10)
    sleep(1)

    # Move servo to 90ï¿½ (1.5 ms pulse)
    print("Moving to 90ï¿½")
    set_angle(90)
    sleep(1)

    # Move servo to 180ï¿½ (2.0 ms pulse)
    print("Moving to 180ï¿½")
    set_angle(180)
    sleep(1)

finally:
    # Clean up and close GPIO
    lgpio.gpio_write(h, SERVO_GPIO, 0)
    lgpio.gpiochip_close(h)
    print("GPIO closed.")
