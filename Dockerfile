# Use a lightweight Python image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app    

# Install Poetry globally
RUN pip install --no-cache-dir poetry

# Prevent Poetry from using a virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy only dependency files first (for better caching)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --only=main --no-interaction --no-ansi   

# Copy the rest of the application
COPY . /app/

# Ensure the application is importable
ENV PYTHONPATH=/app

# Set Python output to be unbuffered (better logging)
ENV PYTHONUNBUFFERED=1

# Expose the Flask application port
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
