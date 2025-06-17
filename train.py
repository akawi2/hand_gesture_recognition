from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# --- Step 1: Define Dataset Class ---
class HandGestureDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = ['Augmenter', 'Defiler_a_droite', 'Defiler_a_gauche', 'Dezoomer', 'Diminuer', 'Zoomer']  # 6 classes
        self.images = []
        
        for label, class_name in enumerate(self.classes):
            class_dir = os.path.join(root_dir, class_name)
            for img_name in os.listdir(class_dir):
                img_path = os.path.join(class_dir, img_name)
                self.images.append((img_path, label))
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path, label = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, label

# --- Step 2: Data Transforms ---
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    # transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# --- Step 3: Create Dataset and Split into Train/Val ---
full_dataset = HandGestureDataset(root_dir='DataSet', transform=train_transform)

# Split dataset (80% train, 20% val)
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])

# Apply val transform to validation set
val_dataset.dataset.transform = val_transform

# --- Step 4: Create Data Loaders ---
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# --- Step 5: Model Setup ---
model = models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, 6)  

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# --- Step 6: Training Setup ---
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# --- Step 7: Train Model ---
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=20):
    train_losses, val_losses = [], []
    train_accuracies, val_accuracies = [], []
    
    best_acc = 0.0
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total_train += labels.size(0)
            correct_train += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / len(train_loader.dataset)
        train_acc = correct_train / total_train
        # Validation
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        val_acc = correct / total
        train_losses.append(epoch_loss)
        val_losses.append(val_loss / len(val_loader.dataset))
        train_accuracies.append(train_acc * 100)  
        val_accuracies.append(val_acc * 100)
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}, Val Acc: {val_acc:.4f}')
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'analysis_best_2.pth')
    
    print(f'Training complete. Best Val Accuracy: {best_acc:.4f}')
    plot_training_results(train_losses, val_losses, train_accuracies, val_accuracies)
    
def plot_training_results(train_losses, val_losses, train_accuracies, val_accuracies):
    epochs = range(1, len(train_losses) + 1)

    plt.figure(figsize=(12, 5))

    # Plot Loss
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_losses, 'r-', label='Training Loss')
    plt.plot(epochs, val_losses, 'b--', label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Over Epochs')
    plt.legend()

    # Plot Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accuracies, 'g-', label='Training Accuracy')
    plt.plot(epochs, val_accuracies, 'm--', label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Over Epochs')
    plt.legend()

    plt.show()
# --- Run Training ---

train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=30)

def evaluate_model(model, test_loader):
    model.eval()
    y_true = []
    y_pred = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            print(f"inputs : {inputs}")
            print(f"labels : {inputs}")
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(predicted.cpu().numpy())
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=['Augmenter', 'Defiler_a_droite', 'Defiler_a_gauche', 'Dezoomer', 'Diminuer', 'Zoomer'])
    
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:\n", report)
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Augmenter', 'Defiler_a_droite', 'Defiler_a_gauche', 'Dezoomer', 'Diminuer', 'Zoomer'], 
                yticklabels=['Augmenter', 'Defiler_a_droite', 'Defiler_a_gauche', 'Dezoomer', 'Diminuer', 'Zoomer'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

# Evaluate the model on validation set
print("\nEvaluation on Validation Set:")
evaluate_model(model, val_loader)


# def evaluate_model(model, test_loader):
#     model.eval()
#     y_true = []
#     y_pred = []
    
#     with torch.no_grad():
#         for inputs, labels in test_loader:
#             inputs, labels = inputs.to(device), labels.to(device)
#             outputs = model(inputs)
#             _, predicted = torch.max(outputs.data, 1)
            
#             y_true.extend(labels.cpu().numpy())
#             y_pred.extend(predicted.cpu().numpy())
    
#     print("Accuracy:", accuracy_score(y_true, y_pred))
#     print("Confusion Matrix:\n", confusion_matrix(y_true, y_pred))
#     print("Classification Report:\n", classification_report(y_true, y_pred, target_names=['normal', 'benign', 'malignant']))

# evaluate_model(model, val_loader)