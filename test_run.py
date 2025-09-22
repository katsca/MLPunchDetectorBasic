import cv2
import mediapipe as mp
import numpy as np
from sklearn.ensemble import RandomForestClassifier  # Change to your trained model
import pickle


punches_name = {
    0: "JAB",  # jab
    1: "CROSS",  # cross
    2: "LEFT HOOK",
    3: "RIGHT HOOK",  # RH
    4: "LEFT UPPER CUT",  # LUC
    5: "RIGHT UPPER CUT",  # RUC
}

# Load your trained model (make sure to pickle it after training!)
with open("punch_model.pkl", "rb") as file:
    model = pickle.load(file)


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


# Initialize the webcam
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()  # Capture frame from webcam
    if not ret:
        break

    # Flip the frame for mirror image effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (MediaPipe requires RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # Draw landmarks on the frame
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    # Extract pose landmarks if available
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extract 99 values (x, y, z for each landmark)
        pose_data = []
        for landmark in landmarks:
            pose_data.extend(
                [landmark.x, landmark.y, landmark.z]
            )  # Flattening pose data

        # Convert the pose data into a numpy array and reshape it
        pose_data = np.array(pose_data).reshape(1, -1)

        # Make predictions using the loaded model
        prediction = model.predict(pose_data)
        punch_type = prediction[0]

        # Display the predicted punch type
        cv2.putText(
            frame,
            f"Punch: {punches_name[punch_type]}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

    # Display the frame with pose landmarks
    cv2.imshow("Punch Detection", frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
