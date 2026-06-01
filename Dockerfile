FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
       pandoc \
       texlive-xetex \
       texlive-latex-recommended \
       texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application
COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "konvertmd.py", "--server.port=8501", "--server.address=0.0.0.0"]
