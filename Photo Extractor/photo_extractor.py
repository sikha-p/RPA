import cv2

# Load the resume image
img = cv2.imread(r'input-image')

# Convert to grayscale (needed for face detection)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load pre-trained Haar cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Detect faces in the image
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),  # Minimum face size to detect (can adjust)
    flags=cv2.CASCADE_SCALE_IMAGE
)

# Check if at least one face is found
if len(faces) == 0:
    print("No face detected in the image.")
else:
    # For this example, we just take the first detected face
    (x, y, w, h) = faces[0]

    # Print coordinates of detected face
    print(f"Face coordinates: x={x}, y={y}, width={w}, height={h}")

    # Crop the detected face region from the original image
    face_img = img[y:y+h, x:x+w]

    # Save the cropped face image
    cv2.imwrite(r'output-image-path', face_img)

    print("Extracted photo saved as 'extracted_photo.jpg'.")
    print("Resume image with detection box saved as 'resume_with_face_box.jpg'.")
