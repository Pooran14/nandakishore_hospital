import cv2

def crop_image(image_path, coord, output_path):
    # Load the image
    (x1, y1, x2, y2) = coord
    image = cv2.imread(image_path)

    # Check if image is loaded properly
    if image is None:
        print("Error: Could not load image. Check the file path.")
        return None

    # Crop the image
    cropped_image = image[y1:y2, x1:x2]

    # Save the cropped image
    cv2.imwrite(output_path, cropped_image)
  
# crop_image(r"E:\poorani project\images\unprocessedimage\sample medicine.jpg",[363,35,387,62],r"E:\poorani project\images\unprocessedimage\sample111.jpg")
