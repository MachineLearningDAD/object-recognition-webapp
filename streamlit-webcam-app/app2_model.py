import cv2
import numpy as np
import onnxruntime
import streamlit as st

# Cargar el modelo YOLOv5 en onnxruntime
session = onnxruntime.InferenceSession('yolov5s.onnx')

# Clases de YOLOv5 (COCO dataset)
CLASSES = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant",
    "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"
]

conf_threshold = 0.3  # Baja el umbral de confianza para obtener más detecciones
nms_threshold = 0.3   # Baja el umbral de supresión no máxima

st.title("Detección de Objetos Cotidianos en Tiempo Real con YOLOv5 y ONNXRuntime")

# Captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("No se pudo abrir la cámara")
else:
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("No se pudo obtener el frame de la cámara")
            break

        # Preprocesamiento para YOLOv5
        img = cv2.resize(frame, (640, 640))
        img = img.transpose((2, 0, 1))  # Cambiar la forma a (C, H, W)
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0

        # Realizar la inferencia
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: img})

        # Obtener detecciones
        boxes, scores, class_ids = [], [], []
        for detection in outputs[0][0]:  # Ajustar según salida del modelo
            score = float(detection[4])
            if score > conf_threshold:
                x1, y1, x2, y2 = int(detection[0]), int(detection[1]), int(detection[2]), int(detection[3])
                boxes.append([x1, y1, x2 - x1, y2 - y1])
                scores.append(score)
                class_ids.append(int(detection[5]))

        # Supresión no máxima
        if boxes:  # Solo aplica NMS si hay detecciones
            indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, nms_threshold)

            # Dibujar resultados si hay índices
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                label = f"{CLASSES[class_ids[i]]}: {scores[i]:.2f}"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Convertir de BGR a RGB para mostrar en Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()
