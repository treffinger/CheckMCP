FROM docker.io/library/python:3.12-slim

WORKDIR /checkmcp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]