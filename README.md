# ML Punch Detector (Basic)
This project uses OpenCV, MediaPipe, scikit-learn, and NumPy to detect and classify different punch types in real-time.
It consists of three main scripts:
1. data_collection.py → Collect punch landmark data using your webcam.
2. data_clean.py → Train a machine learning model to classify punch types.
3. test_run.py → Run real-time punch detection using the trained model.

## SET UP
1. Clone this repository:
```
git clone https://github.com/your-username/MLPunchDetectorBasic.git
cd MLPunchDetectorBasic
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```
3. Install dependencies
```
pip install -r requirements.txt
```
## Project Structure
```
MLPunchDetectorBasic/
│
├─ data_collection.py      # Collect punch data (landmarks → CSV)
├─ data_clean.py           # Train ML model on collected data
├─ test_run.py             # Real-time detection using trained model
├─ models/                 # Saved models (pickle files)
├─ data/                   # Datasets (CSV files)
├─ requirements.txt
└─ README.md
```

## Scripts
### data_collection.py
This script is responsible for collecting training data for different punch types using your webcam, MediaPipe Pose
, and OpenCV. The captured body landmarks are saved into a CSV file, which will later be used for training a machine learning model.

Features:
- Uses MediaPipe Pose to detect body landmarks in real-time.
- Supports six punch types:
  - 1 – Jab
  - 2 – Cross
  - 3 – Left Hook
  - 4 – Right Hook
  - 5 – Left Uppercut
  - 6 – Right Uppercut
- Press 0 to clear the current punch selection.
- Press d to toggle drawing of pose landmarks on the video feed.
- Press q to quit recording.

#### How it works
1. Run the script
```
python data_collection.py
```
2. The webcam feed will open
3. Choose the punch type by pressing number key (1-6)
4. Start performing that punch - the script will record the landmark coordinates and label them with the chosen punch type
5. Repeat for as many punches as you like
6. Quit with q

#### Output:
- A CSV file named punch_data_to_save.csv is generated in data
- Each row contains
  - The punch label (0-5) for 6 punches
  - The x,y,z coords of each pose landmark detected by MediaPipe

The dataset will be used later for training a classifier to recognize punches in real time

### data_clean.py

This script is responsible for training a machine learning model to classify punch types based on the pose landmarks collected with data_collection.py.

Features:
- Loads the punch landmark data from a CSV file (data/punch_data.csv).
- Flattens the pose landmark data to create a suitable feature set for the ML model.
- Splits the dataset into training (80%) and testing (20%) sets.
- Trains a Random Forest classifier using scikit-learn.
- Evaluates the model with:
  - Accuracy on the test set.
  - 5-fold cross-validation across the entire dataset.
- Saves the trained model as a pickle file (models/punch_model.pkl) for later use in real-time detection.

#### How it works
1. Run the script
```
python data_clean.py
```
2. The script loads your collected data (data/punch_data.csv).
3. Data is flattened and split into training and test sets.
4. A Random Forest classifier is trained and evaluated.
5. The trained model is saved to models/punch_model.pkl.

#### Output:
Console output:
- Head of the dataset.
- Shapes of training and test sets.
- Test set accuracy.
- Cross-validation scores and mean accuracy.

File output:
- models/punch_model.pkl — trained Random Forest model ready for real-time prediction.

#### Notes:
- Make sure the data/punch_data.csv file exists (collected with data_collection.py).
- Ensure the models/ directory exists, or the script may fail when saving the pickle file.

### test_run.py
This script is responsible for real-time punch detection using your webcam and the trained machine learning model (models/punch_model.pkl). It leverages MediaPipe Pose to extract body landmarks and Random Forest (or your trained model) to classify punch types.

Features:
- Loads the trained model from models/punch_model.pkl.
- Uses MediaPipe Pose to detect body landmarks in real-time.
- Predicts one of six punch types:
  - 0 – Jab
  - 1 – Cross
  - 2 – Left Hook
  - 3 – Right Hook
  - 4 – Left Uppercut
  - 5 – Right Uppercut
- Displays live predictions directly on the webcam feed.
- Exits when pressing q.

#### How it works:
1. Run the script:
```
python test_run.py
```
2. The webcam feed opens.
3. MediaPipe detects body landmarks for each frame.
4. Landmarks are flattened and fed into the trained model.
5. The predicted punch type is displayed on the video frame.
6. Press q to quit.

#### Output:
- Live video feed with predicted punch type overlaid.
- No files are generated; predictions are displayed in real-time.

#### Notes:
- Make sure the trained model (models/punch_model.pkl) exists before running this script.
- Ensure a webcam is connected and accessible.
- For best results, perform punches clearly in front of the camera and in good lighting.
