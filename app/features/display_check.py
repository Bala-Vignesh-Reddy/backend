import cv2
import base64
import numpy as np
import torch  

def preprocess_image(image):
    """
    Preprocesses the image for the YOLOv5 model.
    """
    resized_image = cv2.resize(image, (640, 640))

    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    normalized_image = rgb_image / 255.0

    batched_image = np.expand_dims(normalized_image, axis=0)

    tensor_image = torch.from_numpy(batched_image).permute(0, 3, 1, 2).float()

    return tensor_image

def run_inference(model, image):
    """
    Runs inference using the YOLOv5 model.
    """
    results = model(image)

    class_index = results.xyxy[0][0][5].item()  

    return class_index

def check_display(frame, model):
    """
    Checks the display for defects using the YOLOv5 model.

    Args:
        frame: The current frame from the camera.
        model: The loaded YOLOv5 model.

    Returns:
        A tuple containing:
            - The processed frame (with annotations if any).
            - An alert message if a defect is found, otherwise None.
    """
    try:
        processed_image = preprocess_image(frame)

        class_index = run_inference(model, processed_image)

        class_labels = ['dark_spot', 'malfunction', 'screen']

        predicted_class = class_labels[int(class_index)]

        cv2.putText(frame, predicted_class, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if predicted_class != 'full_screen':
            alert = f"Display defect detected: {predicted_class}"
        else:
            alert = None

        return frame, alert

    except Exception as e:
        print(f"Error in display check: {e}")
        return frame, "Error during display check"