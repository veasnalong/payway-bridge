FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bridge.py .
COPY bridge_session.session .
CMD ["python", "bridge.py"]
