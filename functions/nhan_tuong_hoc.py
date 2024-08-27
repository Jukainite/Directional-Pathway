import numpy as np
import pandas as pd
import cv2
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
from PIL import Image, ImageColor

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

model_path = r"functions/face_shape_classifier.pth"
train_dataset = {0: 'Khuôn mặt trái tim', 1: 'Khuôn mặt hình chữ nhật_Khuôn mặt dài', 2: 'Khuôn mặt trái xoan',
3: 'Khuôn mặt tròn', 4: 'Khuôn mặt vuông'}

class MyNormalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, tensor):
        # Kiểm tra số kênh của tensor
        if tensor.size(0) == 1:  # Nếu là ảnh xám
            # Thêm một kênh để đảm bảo phù hợp với normalize
            tensor = torch.cat([tensor, tensor, tensor], 0)

        # Normalize tensor
        tensor = transforms.functional.normalize(tensor, self.mean, self.std)
        return tensor


# Load lại mô hình đã được huấn luyện
device = torch.device('cpu')  # Sử dụng CPU
model = torchvision.models.efficientnet_b4(pretrained=False)
num_classes = len(train_dataset)
model.classifier = nn.Sequential(
    nn.Linear(model.classifier[1].in_features, num_classes)
)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# Định nghĩa biến đổi cho ảnh đầu vào
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    MyNormalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_from_image(image):
    # Chuyển ảnh sang grayscale nếu cần thiết
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Chuyển ảnh sang numpy array
    image_np = np.array(image)

    # Chuyển ảnh sang grayscale để sử dụng mô hình nhận diện khuôn mặt
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Nhận diện khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Nếu tìm thấy khuôn mặt, lấy ảnh khuôn mặt và thực hiện dự đoán
    if len(faces) > 0:
        x, y, w, h = faces[0]  # Giả sử chỉ lấy khuôn mặt đầu tiên
        face_img = image.crop((x, y, x + w, y + h))  # Cắt ảnh khuôn mặt từ ảnh gốc

        # Áp dụng biến đổi cho ảnh khuôn mặt
        input_image = transform(face_img).unsqueeze(0)  # Thêm chiều batch (batch size = 1)

        # Thực hiện dự đoán
        with torch.no_grad():
            output = model(input_image)

        # Lấy chỉ số có giá trị lớn nhất là nhãn dự đoán
        predicted_class_idx = torch.argmax(output).item()

        train_dataset = {0: 'Khuôn mặt trái tim', 1: 'Khuôn mặt hình chữ nhật_Khuôn mặt dài', 2: 'Khuôn mặt trái xoan',
                         3: 'Khuôn mặt tròn', 4: 'Khuôn mặt vuông'}
        # Lấy tên của nhãn dự đoán từ tập dữ liệu
        predicted_label = train_dataset[predicted_class_idx]

        return predicted_label
    else:
        return "No face detected."


def predict_from_face_image(image):
    # Áp dụng biến đổi cho ảnh khuôn mặt
    pil_image = Image.fromarray(image)
    input_image = transform(pil_image).unsqueeze(0)  # Thêm chiều batch (batch size = 1)

    # Thực hiện dự đoán
    with torch.no_grad():
        output = model(input_image)

    # Lấy chỉ số có giá trị lớn nhất là nhãn dự đoán
    predicted_class_idx = torch.argmax(output).item()

    train_dataset = {0: 'Khuôn mặt trái tim', 1: 'Khuôn mặt hình chữ nhật_Khuôn mặt dài', 2: 'Khuôn mặt trái xoan',
                     3: 'Khuôn mặt tròn', 4: 'Khuôn mặt vuông'}
    # Lấy tên của nhãn dự đoán từ tập dữ liệu
    predicted_label = train_dataset[predicted_class_idx]

    return predicted_label