# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirments.txt .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirments.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=flaskr
ENV FLASK_ENV=production


# Initialize the database
RUN flask init-db

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "info", "flaskr:create_app()"]