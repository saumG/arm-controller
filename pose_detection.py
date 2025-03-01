import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose and Hands models
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose()
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert image to RGB (MediaPipe expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame for pose and hands
    pose_results = pose.process(rgb_frame)
    hand_results = hands.process(rgb_frame)
    
    h, w, _ = frame.shape
    arm_points = []
    
    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        
        # Get coordinates for arm points
        shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w), 
                    int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h))
        elbow = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * w), 
                 int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * h))
        wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * w), 
                 int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * h))
        
        arm_points = [shoulder, elbow, wrist]
        
        # Draw circles on joints
        cv2.circle(frame, shoulder, 10, (0, 255, 0), -1)
        cv2.circle(frame, elbow, 10, (255, 0, 0), -1)
        cv2.circle(frame, wrist, 10, (0, 0, 255), -1)
        
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Draw arm connections
    if len(arm_points) == 3:
        cv2.line(frame, arm_points[0], arm_points[1], (255, 255, 255), 2)
        cv2.line(frame, arm_points[1], arm_points[2], (255, 255, 255), 2)
    
    # Show the frame
    cv2.imshow('Pose and Finger Detection', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
