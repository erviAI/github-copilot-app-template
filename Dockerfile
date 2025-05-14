# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install --no-dev

# Copy the rest of the application code into the container
COPY . .

# Create a group and a non-root user
RUN groupadd -g 1000 py7-non-root-group
RUN useradd -u 1000 -g py7-non-root-group py7-non-root-user && chown -R 1000 /app

# Set the default user
USER 1000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Expose port 8000
EXPOSE 8000
