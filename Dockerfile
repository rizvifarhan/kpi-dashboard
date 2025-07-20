# Dockerfile for KPI Dashboard
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV STREAMLIT_SERVER_PORT=5000
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]