import os
import tkinter as tk
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image, ImageTk

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ================================
# CARGA DEL MODELO EN FORMATO .PB
# ================================


model_path = "model.savedmodel"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"No se encontró el modelo en la ruta especificada: {model_path}")


model = tf.saved_model.load(model_path)
infer = model.signatures["serving_default"]

# Etiquetas
labels = [
    "0 Completo",
    "1 Incompleto",
    "2 SinSeguridad"
]

# ================================
# CONFIGURACIÓN DE LA CÁMARA
# ================================
camera = cv2.VideoCapture(0) 


def predict_frame(frame):
    """Preprocesa la imagen del frame y realiza la predicción."""
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, axis=0).astype(np.float32) / 255.0

    input_tensor = tf.convert_to_tensor(image)
    predictions = infer(tf.constant(input_tensor))
    output_key = list(predictions.keys())[0]
    probabilities = predictions[output_key].numpy()[0]
    return probabilities


def update_frame():
    
    ret, frame = camera.read()
    if ret:
        frame = cv2.flip(frame, 1)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((350, 350))
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk)
        panel.image = img_tk

        probabilities = predict_frame(frame)
        
        dominant_index = np.argmax(probabilities)
        if dominant_index == 0:
            main_label.config(text="PERMITIDO", fg="#4CAF50")
        else:
            main_label.config(text="NO PERMITIDO", fg="#D32F2F")
        
        #probabilidades
        for i, prob in enumerate(probabilities):
            label_probabilities[i].config(text=f"{labels[i]}: {prob * 100:.2f}%")

    root.after(20, update_frame)  #10 ms


def close_app():
    """Cierra la aplicación y libera la cámara."""
    camera.release()
    root.destroy()


# ================================
# CREACIÓN DE LA INTERFAZ CON TKINTER
# ================================
root = tk.Tk()
root.title("Reconocimiento en Tiempo Real")
root.configure(bg="#F0F0F0")
root.minsize(800, 650)

frame_main = tk.Frame(root, bg="#F0F0F0")
frame_main.pack(pady=10)

panel = tk.Label(frame_main, bg="#FFFFFF", relief="solid", bd=2)
panel.pack()

main_label = tk.Label(root, text="", font=("Arial", 60, "bold"), bg="#F0F0F0")
main_label.pack(pady=20)

frame_labels = tk.Frame(root, bg="#F0F0F0")
frame_labels.pack(pady=10)

label_probabilities = []
for label in labels:
    lbl = tk.Label(frame_labels, text=f"{label}: 0.00%", font=("Arial", 16), fg="#000000", bg="#F0F0F0")
    lbl.pack(anchor='w', padx=20)
    label_probabilities.append(lbl)

btn_exit = tk.Button(root, text="Salir", command=close_app, font=("Arial", 16), bg="#D32F2F", fg="white", relief="raised")
btn_exit.pack(pady=10)

update_frame()
root.mainloop()
