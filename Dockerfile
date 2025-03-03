FROM python:3.11-slim

WORKDIR /opt/docker_data/AsertisBpoIA/ProyectoGeneraAsertisIA

COPY requirements.txt ./ 

COPY . ./

RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
