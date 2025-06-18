# Test file for Hand Gesture Recognition
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

# Load Trained Model
def load_model(model_path, device='cuda' if torch.cuda.is_available() else 'cpu'):
    # Initialize model (same architecture as training)
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 6)  # 6 gesture classes
    
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
    return transform(image).unsqueeze(0)  # Add batch dimension

def predict_image(model, image_tensor, device):
    class_names = ['Augmenter', 'Defiler_a_droite', 'Defiler_a_gauche', 
                   'Dezoomer', 'Diminuer', 'Zoomer']
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        probabilities = torch.softmax(outputs, dim=1)[0] * 100
    return class_names[predicted.item()], probabilities.cpu().numpy()

if __name__ == "__main__":
    MODEL_PATH = 'best_hand_gesture.pth'  # Changed to match training file's saved model
    TEST_IMAGE = "DataSet/Augmenter/IMG-20250502-WA0089.jpg"  # Update with your test image path
    
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
    print(f"\nPrediction: {prediction}")
    print("Confidence Scores:")
    print(f"- Augmenter: {probabilities[0]:.2f}%")
    print(f"- Defiler_a_droite: {probabilities[1]:.2f}%")
    print(f"- Defiler_a_gauche: {probabilities[2]:.2f}%")
    print(f"- Dezoomer: {probabilities[3]:.2f}%")
    print(f"- Diminuer: {probabilities[4]:.2f}%")
    print(f"- Zoomer: {probabilities[5]:.2f}%")