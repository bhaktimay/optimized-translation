FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download model file from Argos website
RUN apt-get update && apt-get install -y wget && \
    wget https://www.argosopentech.com/argospm/packages/translate-en_hi-1_1.argosmodel && \
    apt-get remove -y wget && apt-get clean


COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
