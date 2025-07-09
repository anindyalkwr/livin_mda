# Stage 1: Build the application with dependencies
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY ./requirements.txt .

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Create the final production image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the path to include the venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code into the container
COPY ./app ./app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Uvicorn.
# The host 0.0.0.0 is crucial to make the application accessible from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
