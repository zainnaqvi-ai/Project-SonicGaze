# Project SonicGaze

Project SonicGaze is a real-world hardware/software integration project built for a Digital Logic Design (DLD) university exhibition. It uses AI, Machine Learning, and an Arduino-based circuit to create a biometric security alarm system. 

When an authorized user (trained on local data) is recognized via webcam, the Python script communicates via serial port to an Arduino Uno, triggering a physical LED and buzzer alarm.

##  Tech Stack & Hardware
* **Software:** Python 3.13, OpenCV (`opencv-contrib-python`), PySerial, NumPy.
* **Algorithm:** Haar Cascades (Face Detection) + LBPH (Face Recognition).
* **Hardware:** HP ZBook G10 (Compute/Webcam), Arduino Uno, LED, Buzzer, Breadboard, jumper wires, resistors

## Technical & Ethical Note on LBPH
This project utilizes Local Binary Patterns Histograms (LBPH) for facial recognition. LBPH is highly efficient for edge devices but primarily analyzes localized facial textures and bone structure rather than deep semantic features. 

**Limitation Disclosure:** Because the model is trained entirely on a single authorized user's data (1,030 images), it can occasionally be prone to false positives if an unauthorized person has highly similar localized facial textures. To mitigate this and optimize for strict security, the system's `CONFIDENCE_THRESHOLD` has been rigorously tuned down to **45**. Further tests between **25-35** were also impressive and served full security.  

## Setup & Execution 

*(Note: The `dataset/` and `trainer/` folders are git-ignored to protect biometric data privacy. You must train your own model locally).*

1. **Clone this repository:**
   ````bash
   git clone https://github.com/zainnaqvi-ai/Project-SonicGaze.git
   cd Project-SonicGaze
2. **Create and activate a virtual environment:**
   ````bash
   python -m venv .venv
   .venv\Scripts\activate
3. **Install dependencies and Hardware layer (Arduino code):**
   ````bash
   pip install -r requirements.txt
Open the official Arduino IDE, load arduino_code/alarm_receiver.ino, and upload it directly onto your board. Keep the USB connection intact to allow runtime serial streaming.
4. **Webcam test:**
   ````bash
   python webcam_test.py
5. **Data Collection & Biometric Training:**
   ````bash
   python capture_faces.py
   python train_model.py
6. **Execution:**
   ````bash
   python recognize_and_alert.py

## Author
Built by Syed Ali Zain Naqvi — AI student at UMT, PIAIC AI Architect trainee.
   
