# Sistema de seguridad-Inteligencia Artificial
Sistema de reconocimiento de indumentaria de seguridad.
Este proyecto implementa un sistema de visión por computadora en tiempo real para detectar el uso adecuado de equipo de protección personal (EPP). Utiliza técnicas de Machine Learning y una interfaz sencilla basada en Tkinter para mostrar los resultados.

Tecnologías Utilizadas:
-Python 3.11
-TensorFlow
-OpenCV
-Tkinter
-NumPy
-Pillow

Descripción del Proyecto:
El sistema captura imágenes en tiempo real desde la cámara del dispositivo y realiza una clasificación en tres categorías:

-Completo: El trabajador porta todo el equipo de seguridad requerido.

-Incompleto: El trabajador porta parte del equipo de seguridad.

-Sin Seguridad: El trabajador no porta equipo de seguridad.

El modelo de clasificación fue entrenado previamente y cargado en formato SavedModel (.pb) para inferencia en vivo.

La aplicación muestra:

-Un mensaje grande indicando "PERMITIDO" o "NO PERMITIDO".

-Los porcentajes de predicción para cada clase debajo del mensaje principal.

Mejoras Futuras:
-Añadir detección específica de cada componente del EPP (casco, chaleco, guantes).

-Integrar alertas en tiempo real para incumplimiento de normas de seguridad.

-------------------------------------------------------------------------------------

--MIT.

-Fernando Sejas C.
