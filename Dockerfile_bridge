FROM python:3.12-slim
WORKDIR /app
COPY requirements_bridge.txt .
RUN pip install -r requirements_bridge.txt
COPY bridge.py .
COPY bridge_session.session .
CMD ["python", "bridge.py"]
