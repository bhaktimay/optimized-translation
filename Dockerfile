FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wget for model download
RUN apt-get update && apt-get install -y wget && apt-get clean

# Download and install the translation model
RUN wget https://argos-net.com/v1/translate-en_hi-1_1.argosmodel -O translate-en_hi.argosmodel && \
    argos-translate-cli --install translate-en_hi.argosmodel && \
    rm translate-en_hi.argosmodel

# Copy source code
COPY . .

# Expose port
EXPOSE 5000

# Run the server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
