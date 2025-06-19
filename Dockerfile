FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wget to fetch model from Google Drive
RUN apt-get update && apt-get install -y wget && apt-get clean

# Download Argos model from Google Drive and install it
RUN wget --no-check-certificate "https://drive.google.com/uc?export=download&id=1RM09SaccA4z9gi9_OEFnmu50TdSrnkZF" -O translate-en_hi.argosmodel && \
    python3 -c "import argostranslate.package; argostranslate.package.install_from_path('translate-en_hi.argosmodel')" && \
    rm translate-en_hi.argosmodel

# Copy source code
COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
