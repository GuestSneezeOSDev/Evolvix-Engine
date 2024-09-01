FROM python:3.10-slim
WORKDIR /app
COPY src /app/src
CMD ["python", "src/main.py"]
