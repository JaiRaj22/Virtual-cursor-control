# Use an official Python 3.x image as a base
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app
# Combine copying and installing requirements into a single step
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy the application code
COPY . /app/

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]