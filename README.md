Robot with 10 servos see code import time import math from board import SCL, SDA

import busio from adafruit_pca9685 import PCA9685
Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA) pca = PCA9685(i2c) pca.frequency = 50
Servo mapping
LEFT = {'hip_yaw': 0, 'hip_pitch': 1, 'knee': 2, 'ankle_pitch': 3, 'ankle_roll': 4} 
RIGHT = {'hip_yaw': 5, 'hip_pitch': 6, 'knee': 7, 'ankle_pitch': 8, 'ankle_roll': 9}

#Helper: Set servo angle
def set_servo_angle(channel, angle): 
  pulse = int((angle / 180.0) * 4095) pca.channels[channel].duty_cycle = pulse
  
#Smooth transition using sine interpolation
def smooth_move(channel, start_angle, end_angle, duration=0.5, steps=20): 
  for i in range(steps + 1): 
  t = i / steps # Sine easing: smooth in/out 
  eased = start_angle + (end_angle - start_angle) * (0.5 - 0.5 * math.cos(math.pi * t)) 
  set_servo_angle(channel, eased) time.sleep(duration / steps)
  
#Neutral pose
def neutral_pose(): 
  for ch in range(10): set_servo_angle(ch, 90)
  # Lift leg with balance adjustment
def lift_leg(leg, opposite_leg): 
  # Shift weight to opposite leg 
  smooth_move(opposite_leg['ankle_roll'], 90, 70)  # Lean toward support 
  leg smooth_move(opposite_leg['hip_yaw'], 90, 100)    # Rotate torso slightly

Swing leg forward
def swing_leg(leg): 
  smooth_move(leg['hip_pitch'], 90, 60)

Lower leg and restore balance
def lower_leg(leg, opposite_leg): smooth_move(leg['knee'], 45, 90) 
  smooth_move(leg['hip_pitch'], 60, 90) 
  smooth_move(leg['ankle_pitch'], 120, 90)
  # Restore balance
  smooth_move(opposite_leg['ankle_roll'], 70, 90)
  smooth_move(opposite_leg['hip_yaw'], 100, 90)

Walking cycle
def walk_cycle(): while True: lift_leg(LEFT, RIGHT) swing_leg(LEFT) lower_leg(LEFT, RIGHT)
    lift_leg(RIGHT, LEFT)
    swing_leg(RIGHT)
    lower_leg(RIGHT, LEFT)
try: neutral_pose() walk_cycle() except KeyboardInterrupt: print("Stopping robot...") neutral_pose()
