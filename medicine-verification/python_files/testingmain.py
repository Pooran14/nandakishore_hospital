import easyocr
import cv2
import matplotlib.pyplot as plt

# Initialize EasyOCR Reader (supports multiple languages if needed)
reader = easyocr.Reader(['en'])  # You can add more languages like ['en', 'hi']

# Load Image
image_path = r"E:\poorani project\images\processedimage\sample medicine22.jpg"  # Replace with your image path
image = cv2.imread(image_path)

# Detect Text
results = reader.readtext(image)

# Draw Bounding Boxes on Image
for (bbox, text, prob) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, (top_left[0], top_left[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Display Image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

# Print Extracted Text
for _, text, _ in results:
    print(f"Detected Text: {text}")
