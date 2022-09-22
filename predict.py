import cv2
import numpy as np
import torch
import torchvision
import os

model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(pretrained=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

CLASSES=['Flute',
 'Jakoi',
 'Khaloi',
 'ban bati',
 'Bell Metal Bota',
 'Bell Metal Spoon',
 'bell metal bowl',
 'Bell Metal Plate',
 'Bell Metal Glass',
 'bell metal bota',
 'bell metel cymbal',
 'Jaw harp',
 'Dhol',
 'Pepa',
 'Toka',
 'Julki',
 'Conical Hat']
#COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

model.load_state_dict(torch.load('./model.pth', map_location=device))
model.eval()
detection_threshold = 0.8

def pred(test_image):
    image_name = 'temp'
    if os.path.isfile(f"./outputs/{image_name}.jpg") is True:
        os.remove(f"./outputs/{image_name}.jpg")
    image = cv2.imread(test_image)
    orig_image = image.copy()
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    image = np.transpose(image, (2, 0, 1)).astype(np.float)
    # image = torch.tensor(image, dtype=torch.float).cuda()
    image = torch.tensor(image, dtype=torch.float)
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image)
    outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]
    if len(outputs[0]['boxes']) != 0:
        boxes = outputs[0]['boxes'].data.numpy()
        scores = outputs[0]['scores'].data.numpy()
        boxes = boxes[scores >= detection_threshold].astype(np.int32)
        draw_boxes = boxes.copy()
        pred_classes = [CLASSES[i] for i in outputs[0]['labels'].numpy()]
        
        for j, box in enumerate(draw_boxes):
            cv2.rectangle(orig_image,
                        (int(box[0]), int(box[1])),
                        (int(box[2]), int(box[3])),
                        (0, 0, 255), 2)
            cv2.putText(orig_image, pred_classes[j], 
                        (int(box[0]), int(box[1]-5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 
                        2, lineType=cv2.LINE_AA)
        cv2.imwrite(f"./outputs/{image_name}.jpg", orig_image)
    return f"/outputs/{image_name}.jpg"

