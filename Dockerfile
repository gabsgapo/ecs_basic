FROM python:3

WORKDIR /usr/src/app

# Copiar el archivo.py que queremos ejecutar a la imagen.
COPY app.py ./

# Ejecutar el archivo al iniciar la imagen en un contenedor.
CMD ["python", "./app.py"]
