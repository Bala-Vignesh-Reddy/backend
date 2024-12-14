import cv2
import numpy as np
import base64

def capture_image(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        raise Exception("Unable to capture image")

def add_gridlines(image):
    grid_image = image.copy()
    height, width, _ = grid_image.shape
    for i in range(10, width, 100):
        cv2.line(grid_image, (i, 0), (i, height), (0, 255, 0), 1)
    for i in range(10, height, 100):
        cv2.line(grid_image, (0, i), (width, i), (0, 255, 0), 1)
    return grid_image

def detect_misalignment(image, ref_coords, frame_coords):
    dx = frame_coords[0][0] - ref_coords[0][0]
    dy = frame_coords[0][1] - ref_coords[0][1]
    angle = np.degrees(np.arctan2(dy, dx))
    return angle

def annotate_image(image, angle):
    annotated_image = image.copy()
    text = f"Frame Tilt Detected: {angle:.2f}°"
    cv2.putText(annotated_image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return annotated_image

def check_alignment(camera_id=0):
    try:
        raw_image = capture_image(camera_id)
        image_with_grid = add_gridlines(raw_image)

        ref_coords = [(100, 100), (200, 100), (200, 200), (100, 200)]
        frame_coords = [(100, 100), (200, 110), (200, 210), (100, 200)]
        angle = detect_misalignment(raw_image, ref_coords, frame_coords)

        final_output = annotate_image(image_with_grid, angle)

        _, buffer = cv2.imencode('.jpg', final_output)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        return encoded_image

    except Exception as e:
        print(f"Error: {e}")
        return None
    
if __name__ == '__main__':
    try:
        raw_image = capture_image()
        image_with_grid = add_gridlines(raw_image)
        cv2.imshow("Image with Grid", image_with_grid)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        ref_coords = [(100, 100), (200, 100), (200, 200), (100, 200)]
        frame_coords = [(100,100), (200, 110), (200, 210), (100, 200)]
        angle = detect_misalignment(raw_image, ref_coords, frame_coords)

        final_output = annotate_image(image_with_grid, angle)

        cv2.imshow("Alignment Check", final_output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")    