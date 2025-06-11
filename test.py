import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

# Load Trained Model

def load_model(model_path, device='cuda' if torch.cuda.is_available() else 'cpu'):
    # Initialize model (same architecture as training)
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 3)  # 3 classes: normal, benign, malignant
    
    # Load saved weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()  
    return model

# Image Preprocessing
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)  

def predict_image(model, image_tensor, device):
    class_names = ['normal', 'benign', 'malignant']
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        probabilities = torch.softmax(outputs, dim=1)[0] * 100
    return class_names[predicted.item()], probabilities.cpu().numpy()

if __name__ == "__main__":
    MODEL_PATH = 'best_hand_gesture.pth'
    TEST_IMAGE = 'C:/Users/GLC/Downloads/2.png' 
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    if not os.path.exists(TEST_IMAGE):
        raise FileNotFoundError(f"Test image not found at {TEST_IMAGE}")
    
    # Run prediction
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = load_model(MODEL_PATH, device)
    image_tensor = preprocess_image(TEST_IMAGE)
    prediction, probabilities = predict_image(model, image_tensor, device)
    
    # Print results
    print(f"\nPrediction: {prediction.upper()}")
    print("Confidence Scores:")
    print(f"- Normal: {probabilities[0]:.2f}%")
    print(f"- Benign: {probabilities[1]:.2f}%")
    print(f"- Malignant: {probabilities[2]:.2f}%")
    

