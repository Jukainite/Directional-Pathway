import face_recognition
import cv2
from nhan_tuong_hoc import *

# image = face_recognition.load_image_file("functions/test.jpg")
image = Image.open("functions/test.jpg")
image_np = np.array(image)
# face_locations = face_recognition.face_locations(image)
# # Lấy vị trí của khuôn mặt đầu tiên
# top, right, bottom, left = face_locations[0]

# # Cắt ra khuôn mặt từ ảnh gốc
# face_image = image[top:bottom, left:right]

# Xác định vị trí khuôn mặt trong ảnh
face_locations = face_recognition.face_locations(image_np)

# Lấy vị trí của khuôn mặt đầu tiên
top, right, bottom, left = face_locations[0]

# Cắt ra khuôn mặt từ ảnh gốc
face_image_np = image_np[top:bottom, left:right]

print(predict_from_face_image(face_image_np))
