Face Detection and Cropping from Resume Image
=============================================

This Python script uses OpenCV's Haar Cascade classifier to detect a face in a resume image, then crops and saves the detected face as a separate image.

Features
--------
- Loads an input image (a resume photo).
- Converts the image to grayscale for better face detection.
- Detects faces using a pre-trained Haar Cascade classifier.
- Crops the first detected face region.
- Saves the cropped face image to disk.
- Prints the coordinates of the detected face.

Requirements
------------
- Python 3.x
- OpenCV (cv2) library

Install OpenCV via pip if you haven't already:

    pip install opencv-python

Usage
-----
1. Place your input resume image in your working directory or provide the full path.
2. Modify the script to set:
   - `input-image` to the path of your input image.
   - `output-image-path` to the desired path for the cropped face image.
3. Run the script:

    python face_detection.py

How it works
------------
- The script reads the input image.
- Converts it to grayscale.
- Loads a pre-trained Haar cascade for frontal face detection.
- Detects faces in the grayscale image.
- Crops the first detected face area.
- Saves the cropped face to the output path.

Notes
-----
- If no face is detected, the script will print a message and exit.
- You can customize the face detection parameters (`scaleFactor`, `minNeighbors`, `minSize`) to improve detection for your images.

Example output
--------------
Face coordinates: x=100, y=50, width=80, height=80
Extracted photo saved as 'extracted_photo.jpg'.
Resume image with detection box saved as 'resume_with_face_box.jpg'.
