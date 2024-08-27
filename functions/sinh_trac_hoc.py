import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import cv2

classes = ['Hình cung', 'Vòng tròn hướng tâm', 'Vòng lặp Ulnar', 'Vòm lều', 'Vòng xoáy']

class FingerprintCNN(nn.Module):
    def __init__(self):
        super(FingerprintCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 4 * 4, 128)
        self.fc2 = nn.Linear(128, len(classes))

    def forward(self, x):
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = self.pool(nn.functional.relu(self.conv3(x)))
        x = self.pool(nn.functional.relu(self.conv4(x)))
        x = self.pool(nn.functional.relu(self.conv5(x)))
        x = x.view(-1, 128 * 4 * 4)
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Load the trained model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_fin = FingerprintCNN()
model_fin.load_state_dict(torch.load(r'functions/fingerprint.pth', map_location=device))
model_fin.eval()

# Function to predict label for input image
def predict_label(img):
    # img = cv2.imread(image_path)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img = cv2.resize(img, (128, 128))  # Resize the image to 128x128
    img.reshape(-1, 128, 128, 3)
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    img = transform(img)
    img = img.unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        outputs = model_fin(img)
        _, predicted = torch.max(outputs, 1)
    predicted_class = classes[predicted.item()]
    return predicted_class