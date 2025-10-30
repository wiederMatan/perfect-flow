FROM prefecthq/prefect:3-python3.14-kubernetes

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PREFECT_API_URL=http://prefect-server:4200/api

# Default command
CMD ["prefect", "server", "start", "--host", "0.0.0.0"]
