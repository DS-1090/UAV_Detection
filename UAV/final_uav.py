# -*- coding: utf-8 -*-
"""Final_UAV.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17jPdC-ye_Bz_eKJ8we-Fab0BmZagHHMP
"""

pip install opendatasets

import opendatasets as od

od.download("https://www.kaggle.com/datasets/div456/uav-5000-imgs")

!pip install ultralytics

import ultralytics
import torch

ultralytics.checks()

from ultralytics import YOLO
model = YOLO('yolov8n.pt')

model.summary()

results = model.train(data='/content/uav-5000-imgs/data.yaml',  epochs=18,imgsz=640,batch=-1,save=True,project='/content/output')

!zip -r /content/outputfile.zip /content/output/train3

from google.colab import files
files.download("/content/outputfile.zip")

import torch
torch.save(model.state_dict(), '/content/yolo_model_weights.pth')

files.download("/content/yolo_model_weights.pth")

model.save('/content/saved_model.pt')

files.download("/content/saved_model.pt")

valresults = model.val(data='/content/uav-5000-imgs/data.yaml')

print(valresults)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

images_dir = '/content/uav-5000-imgs/test/images'
annotations_dir = '/content/uav-5000-imgs/test/labels'

image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg'))]

test_image_paths = [os.path.join(images_dir, f) for f in image_files]
annotation_paths = [os.path.join(annotations_dir, f.replace('.jpg', '.txt')) for f in image_files]

# test_image_paths=['/content/uav-yolov8/UAV_YOLOv8/test/images/31cVpQkmEHL_jpg.rf.75c3fff900b3a6f371eb624c96a4a463.jpg']
# annotation_paths=['/content/uav-yolov8/UAV_YOLOv8/test/labels/31cVpQkmEHL_jpg.rf.75c3fff900b3a6f371eb624c96a4a463.txt']
k=0
for i, image_path in enumerate(test_image_paths):
  if(k<10):
      img = Image.open(image_path)
      width, height = img.size

      with open(annotation_paths[i], 'r') as f:
          annotations = f.readlines()

      plt.figure(figsize=(5, 5))
      plt.imshow(img)

      for annotation in annotations:
          parts = annotation.strip().split()
          xgt,ygt,wgt,hgt = map(float, parts[1:5])

          gt_xmin = (xgt-wgt/2)* width
          gt_ymin = (ygt-hgt/2)* height

          gt_rect = patches.Rectangle((gt_xmin, gt_ymin), wgt*width, hgt*height, linewidth=1, edgecolor='g', facecolor='none')
          plt.gca().add_patch(gt_rect)

      results = model(img)
      for result in results:
          boxes = result.boxes.xywh.cpu().numpy()
          confidences = result.boxes.conf.cpu().numpy()  # Extract confidence scores

          for box, conf in zip(boxes, confidences):
              x, y, w, h = box[:4]

              xmin = (x-w/2)
              ymin = (y-h/2)

              rect = patches.Rectangle((xmin, ymin), w , h , linewidth=1, edgecolor='r', facecolor='none')
              plt.gca().add_patch(rect)
              plt.text(xmin, ymin, f'{conf:.2f}', color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))


      plt.axis('off')
      plt.show()
  else:
      break
  k=k+1

import cv2
from google.colab.patches import cv2_imshow

vid = cv2.VideoCapture('/content/Drone Camera ❤️.mp4')

while True:
    ret, frame = vid.read()
    if not ret:
        break

    results = model(frame)

    for result in results:
        boxes = result.boxes.xywh.cpu().numpy()
        for box in boxes:
            x, y, w, h = box[:4]

            xmin = int(x - w/2)
            ymin = int(y - h/2)
            xmax = int(x + w/2)
            ymax = int(y + h/2)

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    cv2_imshow(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()

results = model(["/content/Screenshot 2024-05-22 235923.png", "/content/Screenshot 2024-05-22 235936.png","/content/Screenshot 2024-05-22 235949.png","/content/Screenshot 2024-05-25 184707.png","/content/Screenshot 2024-05-25 184730.png"])
i=0
for result in results:
    boxes = result.boxes
    masks = result.masks
    keypoints = result.keypoints
    probs = result.probs
    obb = result.obb
    result.show()
    result.save(filename="/content/result" + str(i) + ".jpg")
    i=i+1
    print(boxes,masks,keypoints,probs,obb)



model.info()

# from ultralytics import YOLO
# model = YOLO('yolov8n.pt')

# model = model.load('/content/saved_model.pt')

results = model(["/content/Screenshot 2024-05-25 193620.png"])
i=0
for result in results:
    result.show()
    result.save(filename="/content/result"+".jpg")

!yolo task=detect mode=predict model={HOME}/runs/detect/train/weights/best.pt conf=0.25 source={dataset.location}/test/images save=True

project.version(dataset.version).deploy(model_type="yolov8", model_path=f"{HOME}/runs/detect/train/")

model = YOLO("/content/best.pt")