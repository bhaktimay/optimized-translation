FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wget for model download
RUN apt-get update && apt-get install -y wget && apt-get clean

# Download the Argos model
RUN wget https://argos-net.com/v1/translate-en_hi-1_1.argosmodel -O translate-en_hi.argosmodel

# Use Python to install the model instead of CLI
RUN python3 -c "import argostranslate.package, argostranslate.translate; \
pkg = argostranslate.package.Package.load('translate-en_hi.argosmodel'); \
argostranslate.package.install_from_path('translate-en_hi.argosmodel')"

# Remove model file to keep image small
RUN rm translate-en_hi.argosmodel

# Copy the rest of the code
COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
