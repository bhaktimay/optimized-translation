FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download and install Argos model
RUN wget https://argos-net.com/v1/translate-en_hi-1_1.argosmodel -O translate-en_hi.argosmodel && \
    argos-translate-cli --install translate-en_hi.argosmodel && \
    rm translate-en_hi.argosmodel



COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
