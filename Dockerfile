# Simple Dockerfile to run the demo and Streamlit dashboard
FROM python:3.13-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies needed for demo + dashboard
RUN pip install --no-cache-dir streamlit pydantic pandas

# Copy app sources
COPY . /app

# Expose Streamlit port
EXPOSE 8501

# Run demo to generate sample outputs then start Streamlit
CMD ["/bin/sh", "-c", "python run_demo.py && streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0"]
