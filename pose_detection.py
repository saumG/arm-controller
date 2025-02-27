import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose and Hands models
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_hands = mp.solutions.hands
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
    
    # Process frame for pose and hand landmarks
    pose_results = pose.process(rgb_frame)
    hand_results = hands.process(rgb_frame)
    
    if pose_results.pose_landmarks:
        # Draw pose landmarks on the frame
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Extract important joint positions (shoulder, elbow, wrist)
        landmarks = pose_results.pose_landmarks.landmark
        
        # Get coordinates (normalized values: 0 to 1, so we scale them to image size)
        h, w, _ = frame.shape
        shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w), 
                    int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h))
        elbow = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * w), 
                 int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * h))
        wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * w), 
                 int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * h))
        
        # Draw circles on joints
        cv2.circle(frame, shoulder, 10, (0, 255, 0), -1)
        cv2.circle(frame, elbow, 10, (255, 0, 0), -1)
        cv2.circle(frame, wrist, 10, (0, 0, 255), -1)
        
        # Calculate elbow angle
        def calculate_angle(a, b, c):
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            
            ba = a - b
            bc = c - b
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
            return np.degrees(angle)
        
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        # Display angle on screen
        cv2.putText(frame, f'Elbow Angle: {int(elbow_angle)}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Process hands
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get the index finger tip position
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            
            # Draw index finger tip
            cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)
            cv2.putText(frame, f'Index: ({x}, {y})', (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Show the frame
    cv2.imshow('Pose and Finger Detection', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
