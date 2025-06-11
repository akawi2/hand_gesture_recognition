import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

# Load the PyTorch model
model = models.resnet18(pretrained=False)  # Same architecture as during training
model.fc = nn.Linear(model.fc.in_features, 6)  # Important: Match the final layer
model.load_state_dict(torch.load('best_hand_gesture.pth', map_location=torch.device('cpu')))
model.eval()  # Set to evaluation mode

class_names = ['Augmenter', 'Defiler a droite', 'Defiler a gauche', 'Dezoomer', 'Diminuer', 'Zommer']

# Color scheme for visualization
COLORS = {
    'text': (0, 255, 0),        # Green
    'high_confidence': (0, 255, 0),  # Green
    'medium_confidence': (0, 255, 255), # Yellow
    'low_confidence': (0, 0, 255)    # Red
}

# Use the same transforms as your validation data
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def preprocess_frame(frame):
    """Prepare frame for model prediction"""
    # Convert to PIL Image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame)
    
    # Apply transformations
    tensor = transform(pil_image)
    
    # Add batch dimension
    tensor = tensor.unsqueeze(0)
    
    return tensor

def get_confidence_color(confidence):
    """Determine color based on confidence level"""
    if confidence > 0.7:
        return COLORS['high_confidence']
    elif confidence > 0.4:
        return COLORS['medium_confidence']
    else:
        return COLORS['low_confidence']

def draw_prediction(frame, class_name, confidence):
    """Draw prediction information on frame"""
    # Get appropriate color
    color = get_confidence_color(confidence)
    
    # Main prediction text
    prediction_text = f"{class_name} ({confidence:.0%})"
    cv2.putText(frame, prediction_text, 
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                1, color, 2, cv2.LINE_AA)
    
    # Confidence bar
    bar_width = 200
    bar_height = 20
    bar_x = 20
    bar_y = 70
    
    # Background bar
    cv2.rectangle(frame, (bar_x, bar_y), 
                 (bar_x + bar_width, bar_y + bar_height),
                 (50, 50, 50), -1)
    
    # Filled confidence bar
    filled_width = int(bar_width * confidence)
    cv2.rectangle(frame, (bar_x, bar_y), 
                 (bar_x + filled_width, bar_y + bar_height),
                 color, -1)
    
    # Border for bar
    cv2.rectangle(frame, (bar_x, bar_y), 
                 (bar_x + bar_width, bar_y + bar_height),
                 (255, 255, 255), 1)
    
    return frame

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Create a copy for display
    display_frame = frame.copy()
    
    # Preprocess and predict
    input_tensor = preprocess_frame(frame)
    
    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_class = torch.max(probabilities, 0)
        confidence = confidence.item()
        predicted_class = predicted_class.item()
    
    # Draw prediction information
    display_frame = draw_prediction(display_frame, 
                                  class_names[predicted_class], 
                                  confidence)
    
    # Display all class probabilities (optional)
    y_offset = 120
    for i, (name, prob) in enumerate(zip(class_names, probabilities)):
        color = COLORS['text'] if i == predicted_class else (200, 200, 200)
        text = f"{name}: {prob:.1%}"
        cv2.putText(display_frame, text, 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, color, 1, cv2.LINE_AA)
        y_offset += 30
    
    # Show frame
    cv2.imshow('Hand Gesture Recognition', display_frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()