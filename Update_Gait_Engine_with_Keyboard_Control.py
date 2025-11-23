import time
import math
from pynput import keyboard
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Servo mapping
servo_map = {
    "left_hip_x": 0,
    "left_hip_y": 1,
    "left_knee": 2,
    "left_ankle": 3,
    "right_hip_x": 4,
    "right_hip_y": 5,
    "right_knee": 6,
    "right_ankle": 7,
    "torso": 8,
    "kick_leg": 9
}

# Gait parameters (modifiable in real-time)
gait_params = {
    "step_length": 30,   # degrees
    "lift_height": 30,   # degrees
    "step_duration": 0.3 # seconds
}

# Convert angle to PWM duty cycle
def angle_to_duty(angle):
    min_dc = int((0.5 / 20.0) * 4095)
    max_dc = int((2.5 / 20.0) * 4095)
    return int(min_dc + (angle / 180.0) * (max_dc - min_dc))

# Smooth move
def smooth_move(name, start_angle, end_angle, duration=0.5, steps=20):
    channel = servo_map[name]
    for i in range(steps + 1):
        t = i / steps
        eased = start_angle + (end_angle - start_angle) * (0.5 - 0.5 * math.cos(math.pi * t))
        pca.channels[channel].duty_cycle = angle_to_duty(eased)
        time.sleep(duration / steps)

# Gait primitives
def lift_leg(side="left"):
    smooth_move(f"{side}_hip_y", 90, 90 - gait_params["lift_height"], gait_params["step_duration"])
    smooth_move(f"{side}_knee", 90, 90 + gait_params["lift_height"], gait_params["step_duration"])

def place_leg(side="left"):
    smooth_move(f"{side}_knee", 90 + gait_params["lift_height"], 90, gait_params["step_duration"])
    smooth_move(f"{side}_hip_y", 90 - gait_params["lift_height"], 90, gait_params["step_duration"])

def step_forward(side="left"):
    lift_leg(side)
    smooth_move(f"{side}_hip_x", 90, 90 - gait_params["step_length"], gait_params["step_duration"])
    place_leg(side)
    smooth_move(f"{side}_hip_x", 90 - gait_params["step_length"], 90, gait_params["step_duration"])

def kick_ball():
    lift_leg("kick_leg")
    smooth_move("kick_leg", 90, 30, 0.2)
    smooth_move("kick_leg", 30, 90, 0.2)

# Keyboard listener
def on_press(key):
    try:
        if key.char == 'w':
            gait_params["step_length"] += 5
        elif key.char == 's':
            gait_params["step_length"] -= 5
        elif key.char == 'a':
            gait_params["lift_height"] += 5
        elif key.char == 'd':
            gait_params["lift_height"] -= 5
        elif key.char == '+':
            gait_params["step_duration"] = max(0.1, gait_params["step_duration"] - 0.05)
        elif key.char == '-':
            gait_params["step_duration"] += 0.05
        print(f"Gait updated: {gait_params}")
    except AttributeError:
        pass

def walk_cycle(steps=10):
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    for _ in range(steps):
        step_forward("left")
        step_forward("right")
    listener.stop()

def play_soccer():
    walk_cycle(4)
    kick_ball()