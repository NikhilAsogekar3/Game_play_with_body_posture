# Name - Nikhil Narayan Asogekar (MTech IISc Bangalore)
# Date - 1 June 2021

import cv2
import mediapipe as mp
import numpy as np
from tkinter import *
import random
import time

player_name = "Nikhil"
speed_level = 1 # Choose between 1, 2, and 3.

# Constants ------------------------------------------------------------------------------------------------------------
head_size = 100
neck_size = 10
eye_size = 10
sholder_length = 100
body_height = 200
fingure_size = 10
Body_parts = []
draw_man = FALSE

# Canvas settings ------------------------------------------------------------------------------------------------------
tk = Tk()

WIDTH = 800
HEIGHT = 500

canvas = Canvas(tk, width = WIDTH, height = HEIGHT)
tk.title("Nik")
canvas.pack()

# Pose detection -------------------------------------------------------------------------------------------------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Game pre-requisites --------------------------------------------------------------------------------------------------
if speed_level == 1:
  x_speed = 10
  y_speed = 10

if speed_level == 2:
  x_speed = 15
  y_speed = 15

if speed_level > 2:
  x_speed = 20
  y_speed = 20

stick_height = 20
stick_length = 120

score = 0

ball_1 = canvas.create_oval(50, 50, 100, 100, fill = "black")
rect = canvas.create_rectangle(stick_height, stick_height, WIDTH - stick_height, HEIGHT - stick_height)
text = canvas.create_text(WIDTH*4/5, 10, fill="darkblue", font="Times 20 italic bold", text="Player: {}".format(player_name))

## Setup mediapipe instance --------------------------------------------------------------------------------------------
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    ret, frame = cap.read()

    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    head = [-300, -300]
    R_hand_mid = [-300, -300]
    R_hand_end = [-300, -300]
    L_hand_mid = [-300, -300]
    L_hand_end = [-300, -300]
    R_leg_mid = [-300, -300]
    R_leg_end = [-300, -300]
    L_leg_mid = [-300, -300]
    L_leg_end = [-300, -300]

    # Extract landmarks ------------------------------------------------------------------------------------------------
    try:
      landmarks = results.pose_landmarks.landmark

      head = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.NOSE.value].x), HEIGHT * landmarks[mp_pose.PoseLandmark.NOSE.value].y]

      L_hand_mid = [WIDTH *(1- landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x), HEIGHT * landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
      L_hand_end = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x), HEIGHT * landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

      R_hand_mid = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x), HEIGHT * landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
      R_hand_end = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x), HEIGHT * landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

      L_leg_mid = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x), HEIGHT * landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
      L_leg_end = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x), HEIGHT * landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

      R_leg_mid = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x), HEIGHT * landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
      R_leg_end = [WIDTH * (1-landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x), HEIGHT * landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    except:
      pass

    # Render detections ------------------------------------------------------------------------------------------------
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )
    # Head -------------------------------------------------------------------------------------------------------------
    head_r = head_size / 2

    head_x1 = head[0] - head_r
    head_y1 = head[1] - head_r
    head_x2 = head_x1 + head_size
    head_y2 = head_y1 + head_size

    head_center_x = head_x1 + head_r
    head_center_y = head_y1 + head_r

    # Smile ------------------------------------------------------------------------------------------------------------
    smile_x1 = head_center_x - 10
    smile_y1 = head_center_y + head_r/2
    smile_x2 = head_center_x + 10
    smile_y2 = head_center_y + head_r/2 + 10

    # Neck -------------------------------------------------------------------------------------------------------------
    neck_mid_x = head_center_x
    neck_mid_y = head_center_y + head_r

    neck_x1 = neck_mid_x - 5
    neck_y1 = neck_mid_y
    neck_x2 = neck_mid_x + 5
    neck_y2 = neck_mid_y + neck_size

    # Eyes -------------------------------------------------------------------------------------------------------------
    L_eye_x2 = head_center_x - head_r / 2
    L_eye_y2 = head_center_y
    L_eye_x1 = L_eye_x2 - eye_size
    L_eye_y1 =L_eye_y2 - eye_size

    R_eye_x2 = head_center_x + head_r / 2
    R_eye_y2 = head_center_y
    R_eye_x1 = R_eye_x2 + eye_size
    R_eye_y1 = R_eye_y2 - eye_size

    # Sholder ----------------------------------------------------------------------------------------------------------
    sholder_mid_x = head_center_x
    sholder_mid_y = head_center_y + head_r + neck_size
    sholder_x1 = sholder_mid_x - (sholder_length / 2)
    sholder_y1 = sholder_mid_y
    sholder_x2 = sholder_mid_x + (sholder_length / 2)
    sholder_y2 = sholder_mid_y

    # Body -------------------------------------------------------------------------------------------------------------
    body_y2 = sholder_y2 + body_height

    # Hands ------------------------------------------------------------------------------------------------------------
    L_hand_x = sholder_x1
    L_hand_y = sholder_y1
    R_hand_x = sholder_x2
    R_hand_y = sholder_y2

    L_hand_mid_x = L_hand_mid[0]
    L_hand_mid_y = L_hand_mid[1]
    L_hand_end_x = L_hand_end[0]
    L_hand_end_y = L_hand_end[1]

    R_hand_mid_x = R_hand_mid[0]
    R_hand_mid_y = R_hand_mid[1]
    R_hand_end_x = R_hand_end[0]
    R_hand_end_y = R_hand_end[1]

    # Hand Fingers -----------------------------------------------------------------------------------------------------
    Lh_fingure_x1 = L_hand_end_x - fingure_size
    Lh_fingure_y1 = L_hand_end_y - fingure_size
    Lh_fingure_x2 = L_hand_end_x + fingure_size
    Lh_fingure_y2 = L_hand_end_y + fingure_size

    Rh_fingure_x1 = R_hand_end_x - fingure_size
    Rh_fingure_y1 = R_hand_end_y - fingure_size
    Rh_fingure_x2 = R_hand_end_x + fingure_size
    Rh_fingure_y2 = R_hand_end_y + fingure_size

    # Legs -------------------------------------------------------------------------------------------------------------
    L_leg_x = sholder_x1
    L_leg_y = sholder_y1 + body_height

    R_leg_x = sholder_x2
    R_leg_y = sholder_y2 + body_height

    L_leg_mid_x = L_leg_mid[0]
    L_leg_mid_y = L_leg_mid[1]
    L_leg_end_x = L_leg_end[0]
    L_leg_end_y = L_leg_end[1]

    R_leg_mid_x = R_leg_mid[0]
    R_leg_mid_y = R_leg_mid[1]
    R_leg_end_x = R_leg_end[0]
    R_leg_end_y = R_leg_end[1]

    # Leg Fingers ------------------------------------------------------------------------------------------------------
    Ll_fingure_x1 = L_leg_end_x - fingure_size
    Ll_fingure_y1 = L_leg_end_y - fingure_size
    Ll_fingure_x2 = L_leg_end_x + fingure_size
    Ll_fingure_y2 = L_leg_end_y + fingure_size

    Rl_fingure_x1 = R_leg_end_x - fingure_size
    Rl_fingure_y1 = R_leg_end_y - fingure_size
    Rl_fingure_x2 = R_leg_end_x + fingure_size
    Rl_fingure_y2 = R_leg_end_y + fingure_size

    if draw_man == TRUE:
      head = canvas.create_oval(head_x1, head_y1, head_x2, head_y2, fill="pink")
      hairs = canvas.create_arc(head_x1, head_y1, head_x2, head_y2 - 3 * eye_size, start=0, extent=180, fill="black")
      smile = canvas.create_arc(smile_x1, smile_y1, smile_x2, smile_y2, start=0, extent=-180, fill="black")

      neck = canvas.create_rectangle(neck_x1, neck_y1, neck_x2, neck_y2)
      L_eye = canvas.create_oval(L_eye_x1, L_eye_y1, L_eye_x2, L_eye_y2, fill="blue")
      R_eye = canvas.create_oval(R_eye_x1, R_eye_y1, R_eye_x2, R_eye_y2, fill="blue")

      body = canvas.create_rectangle(sholder_x1, sholder_y1, sholder_x2, body_y2)

      Left_hand_mid = canvas.create_line(L_hand_x, L_hand_y, L_hand_mid_x, L_hand_mid_y)
      Left_hand_end = canvas.create_line(L_hand_mid_x, L_hand_mid_y, L_hand_end_x, L_hand_end_y)
      Right_hand_mid = canvas.create_line(R_hand_x, R_hand_y, R_hand_mid_x, R_hand_mid_y)
      Right_hand_end = canvas.create_line(R_hand_mid_x, R_hand_mid_y, R_hand_end_x, R_hand_end_y)

      Lh_fingures = canvas.create_oval(Lh_fingure_x1, Lh_fingure_y1, Lh_fingure_x2, Lh_fingure_y2, fill="black")
      Rh_fingures = canvas.create_oval(Rh_fingure_x1, Rh_fingure_y1, Rh_fingure_x2, Rh_fingure_y2, fill="black")

      Left_leg_mid = canvas.create_line(L_leg_x, L_leg_y, L_leg_mid_x, L_leg_mid_y)
      Left_leg_end = canvas.create_line(L_leg_mid_x, L_leg_mid_y, L_leg_end_x, L_leg_end_y)
      Right_leg_mid = canvas.create_line(R_leg_x, R_leg_y, R_leg_mid_x, R_leg_mid_y)
      Right_leg_end = canvas.create_line(R_leg_mid_x, R_leg_mid_y, R_leg_end_x, R_leg_end_y)

      Ll_fingures = canvas.create_oval(Ll_fingure_x1, Ll_fingure_y1, Ll_fingure_x2, Ll_fingure_y2, fill="black")
      Rl_fingures = canvas.create_oval(Rl_fingure_x1, Rl_fingure_y1, Rl_fingure_x2, Rl_fingure_y2, fill="black")

      # Body parts -----------------------------------------------------------------------------------------------------
      Body_parts = [head, hairs, smile, neck, L_eye, R_eye, body, Left_hand_mid, Left_hand_end, Right_hand_mid,
                  Right_hand_end, Lh_fingures, Rh_fingures, Left_leg_mid, Left_leg_end, Right_leg_mid,
                  Right_leg_end, Ll_fingures, Rl_fingures]

    # Game loop --------------------------------------------------------------------------------------------------------

    # Horizontal Sticks ------------------------------------------------------------------------------------------------
    stick_1_x1 = head_x1
    stick_1_y1 = HEIGHT - stick_height
    stick_1_x2 = stick_1_x1 + stick_length
    stick_1_y2 = HEIGHT

    stick_1 = canvas.create_rectangle(stick_1_x1, stick_1_y1, stick_1_x2, stick_1_y2, fill="red") # Bottom
    stick_2 = canvas.create_rectangle(stick_1_x1, 0, stick_1_x2, stick_height, fill="red") # Top

    # Vertical Sticks --------------------------------------------------------------------------------------------------
    stick_3_x1 = WIDTH - stick_height
    stick_3_y1 = R_hand_end_y
    stick_3_x2 = WIDTH
    stick_3_y2 = stick_3_y1 + stick_length

    stick_4_x1 = 0
    stick_4_y1 = L_hand_end_y
    stick_4_x2 = stick_height
    stick_4_y2 = stick_4_y1 + stick_length

    stick_3 = canvas.create_rectangle(stick_3_x1, stick_3_y1, stick_3_x2, stick_3_y2, fill="red") # Right
    stick_4 = canvas.create_rectangle(stick_4_x1, stick_4_y1, stick_4_x2, stick_4_y2, fill="red") # Left

    # Ball -------------------------------------------------------------------------------------------------------------
    canvas.move(ball_1, x_speed, y_speed)

    pos_stick_1 = canvas.coords(stick_1)
    pos_stick_2 = canvas.coords(stick_2)
    pos_stick_3 = canvas.coords(stick_3)
    pos_stick_4 = canvas.coords(stick_4)

    pos_ball = canvas.coords(ball_1)

    # Horizontal sticks control ----------------------------------------------------------------------------------------
    if pos_stick_1[1] <= pos_ball[3]:
      if pos_stick_1[0] <= pos_ball[2] and pos_stick_1[2] >= pos_ball[0]:
        y_speed = -(y_speed + 1)
        score += 1

      else:
        y_speed = -(y_speed - 1)
        score -= 1

    if pos_stick_2[3] >= pos_ball[1]:
      if pos_stick_2[0] <= pos_ball[2] and pos_stick_2[2] >= pos_ball[0]:
        y_speed = -(y_speed + 1)
        score += 1

      else:
        y_speed = -(y_speed - 1)
        score -= 1

    # Vertical sticks control ------------------------------------------------------------------------------------------
    if pos_stick_3[0] <= pos_ball[2]:
      if pos_stick_3[1] <= pos_ball[1] and pos_stick_3[3] >= pos_ball[3]:
        x_speed = -(x_speed + 1)
        score += 1

      else:
        x_speed = -(x_speed - 1)
        score -= 1

    if pos_stick_4[2] >= pos_ball[0]:
      if pos_stick_4[1] <= pos_ball[1] and pos_stick_4[3] >= pos_ball[3]:
        x_speed = -(x_speed + 1)
        score += 1

      else:
        x_speed = -(x_speed - 1)
        score -= 1

    # If ball moves out of canvas --------------------------------------------------------------------------------------
    if pos_ball[1] <= -200 or pos_ball[3] >= HEIGHT + 200:
      canvas.delete(ball_1)
      ball_1 = canvas.create_oval(50, 50, 100, 100, fill = "black")

    if pos_ball[0] <= -200 or pos_ball[2] >= WIDTH + 200:
      canvas.delete(ball_1)
      ball_1 = canvas.create_oval(50, 50, 100, 100, fill = "black")


    text = canvas.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text="Score = {}".format(score))

    tk.update()
    time.sleep(0.01)

    sticks = [stick_1, stick_2, stick_3, stick_4]

   # Delete parts -------------------------------------------------------------------------------------------------------
    for i in Body_parts:
      canvas.delete(i)

    for j in sticks:
      canvas.delete(j)

    canvas.delete(text)

   # Flip and show image ------------------------------------------------------------------------------------------------
    image = cv2.flip(image, 1)
    cv2.imshow('Nikhil', image)

    # Close ------------------------------------------------------------------------------------------------------------
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break

  canvas.mainloop()
  cap.release()
  cv2.destroyAllWindows()




