import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard for PWM servos

# Helper: Convert angle to duty cycle
def set_servo_angle(channel, angle):
    pulse = int((angle / 180.0) * 4095)
    pca.channels[channel].duty_cycle = pulse

# Define servo channels
LEFT = {'hip_yaw': 0, 'hip_pitch': 1, 'knee': 2, 'ankle_pitch': 3, 'ankle_roll': 4}
RIGHT = {'hip_yaw': 5, 'hip_pitch': 6, 'knee': 7, 'ankle_pitch': 8, 'ankle_roll': 9}

# Neutral pose
def neutral_pose():
    for ch in range(10):
        set_servo_angle(ch, 90)  # Midpoint angle

# Lift leg
def lift_leg(leg):
    set_servo_angle(leg['knee'], 45)         # Bend knee
    set_servo_angle(leg['ankle_pitch'], 120) # Tilt foot
    time.sleep(0.2)

# Swing leg forward
def swing_leg(leg):
    set_servo_angle(leg['hip_pitch'], 60)    # Move leg forward
    time.sleep(0.2)

# Lower leg
def lower_leg(leg):
    set_servo_angle(leg['knee'], 90)         # Straighten knee
    set_servo_angle(leg['hip_pitch'], 90)    # Return hip
    set_servo_angle(leg['ankle_pitch'], 90)  # Reset foot
    time.sleep(0.2)

# Basic walking cycle
def walk_cycle():
    while True:
        lift_leg(LEFT)
        swing_leg(LEFT)
        lower_leg(LEFT)

        lift_leg(RIGHT)
        swing_leg(RIGHT)
        lower_leg(RIGHT)

try:
    neutral_pose()
    walk_cycle()
except KeyboardInterrupt:
    print("Stopping robot...")
    neutral_pose()