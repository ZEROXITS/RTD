FROM python:3.12-slim

WORKDIR /app/RTD

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN pip install --no-cache-dir uv

# Copy project files
COPY . .

# Install Python dependencies
RUN uv pip install --system -r requirements.txt
RUN uv pip install --system gradio

# Expose Gradio port
EXPOSE 7860

# Default command to run the web UI
CMD ["python", "web_ui.py"]
