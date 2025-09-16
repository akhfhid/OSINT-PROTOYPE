import onnxruntime as ort
from PIL import Image
import numpy as np

LABELS = ["drugs", "weapon", "nsfw", "normal"]


def predict(image_path):
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    arr = np.array(img).astype("float32") / 255.0
    arr = np.transpose(arr, (2, 0, 1))
    arr = np.expand_dims(arr, axis=0)

    sess = ort.InferenceSession("models/mobilenetv2.onnx")
    input_name = sess.get_inputs()[0].name
    preds = sess.run(None, {input_name: arr})[0][0]
    return {LABELS[i]: float(preds[i]) for i in range(len(LABELS))}
