import cv2
import csv
import mediapipe as mp

# Initialise the pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Define punch motions
punch_types = [
    "Jab",
    "Cross",
    "Left Hook",
    "Right Hook",
    "Left Uppercut",
    "Right Uppercut",
]
punch_label = None  # Label for the current punch type

# Start video capture
cap = cv2.VideoCapture(0)

# Prepare to save data
data = []
draw = False
frame_count = 0
print("Press the number (1-6) for the punch type and 'q' to quit:")
for i, punch in enumerate(punch_types):
    print(f"{i+1}: {punch}")


while cap.isOpened():
    ret, frame = cap.read()
    # If not recording then just quit
    if not ret:
        break
    # ELSE

    # Display the current punch type
    frame = cv2.flip(frame, 1)  # Flip horizontally for a mirror effect
    # If recording
    if punch_label is not None:
        cv2.putText(
            frame,
            f"Recording: {punch_types[punch_label]}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
    # If nothing selected
    else:
        cv2.putText(
            frame,
            "Press 1-6 to select punch type",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    # Pose Detection
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Draw landmarks on the frame
    if results.pose_landmarks and draw:
        mp_drawing.draw_landmarks(
            frame,  # pass through our image
            results.pose_landmarks,  #
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(
                color=(245, 117, 66), thickness=2, circle_radius=2
            ),  # drawing spec
            mp_drawing.DrawingSpec(color=(245, 66, 280), thickness=2, circle_radius=2),
        )

    # Extract pose landmarks
    if results.pose_landmarks and punch_label is not None:
        landmarks = [(lm.x, lm.y, lm.z) for lm in results.pose_landmarks.landmark]
        data.append([punch_label] + [coord for lm in landmarks for coord in lm])
        frame_count += 1

    # Key bindings
    key = cv2.waitKey(10) & 0xFF
    if key == ord("q"):  # Quit
        break
    elif ord("1") <= key <= ord("6"):  # Select punch type
        punch_label = key - ord("1")  # Map to 0-5
        print(f"Selected: {punch_types[punch_label]}")
    elif key == ord("0"):
        punch_label = None
    elif key == ord("d"):
        draw = not draw

    # Display the video feed
    cv2.imshow("Data Collection", frame)

cap.release()
cv2.destroyAllWindows()


# Save collected data to CSV
print(f"Collected {frame_count} frames of data.")
with open("punch_data_to_save.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
print("Data saved to punch_data_to_save.csv")
