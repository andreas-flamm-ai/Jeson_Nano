import time
import math
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard servo frequency

# Convert angle (0–180°) to PWM duty cycle (0–4095)
def angle_to_duty_cycle(angle):
    min_pulse = 0.5  # milliseconds
    max_pulse = 2.5  # milliseconds
    pulse_range = max_pulse - min_pulse
    pulse = min_pulse + (angle / 180.0) * pulse_range
    duty_cycle = int((pulse / 20.0) * 4095)  # 20ms period at 50Hz
    return duty_cycle

# Smoothly move servo from start_angle to end_angle
def smooth_move(channel, start_angle, end_angle, duration=1.0, steps=30):
    for i in range(steps + 1):
        t = i / steps
        # Sine easing for smooth acceleration/deceleration
        eased_angle = start_angle + (end_angle - start_angle) * (0.5 - 0.5 * math.cos(math.pi * t))
        duty = angle_to_duty_cycle(eased_angle)
        pca.channels[channel].duty_cycle = duty
        time.sleep(duration / steps)


def lift_leg(leg, opposite_leg):
    # Pre-tilt torso and shift weight to support leg
    smooth_move(opposite_leg['ankle_roll'], 90, 65)     # Deeper lean
    smooth_move(opposite_leg['hip_yaw'], 90, 105)       # Rotate torso more
    time.sleep(0.1)                                     # Let body settle

    # Lift active leg slowly
    smooth_move(leg['knee'], 90, 50, duration=0.6)
    smooth_move(leg['ankle_pitch'], 90, 115, duration=0.6)

def swing_leg(leg):
    # Reduce swing amplitude to avoid tipping
    smooth_move(leg['hip_pitch'], 90, 70, duration=0.5)

def lower_leg(leg, opposite_leg):
    # Lower slowly to avoid shock
    smooth_move(leg['knee'], 50, 90, duration=0.6)
    smooth_move(leg['hip_pitch'], 70, 90, duration=0.5)
    smooth_move(leg['ankle_pitch'], 115, 90, duration=0.5)

    # Restore balance slowly
    smooth_move(opposite_leg['ankle_roll'], 65, 90, duration=0.4)
    smooth_move(opposite_leg['hip_yaw'], 105, 90, duration=0.4)

