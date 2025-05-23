# Use an official Python runtime as a parent image
FROM python:3.12.4-slim
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Git
RUN apt-get update && apt-get install -y git

# Install any needed packages specified in requirements.txt
# RUN pip install git+https://github.com/kramcat/CharacterAI.git 
RUN pip install --no-cache-dir -r requirements.txt
# Make port 8765 available to the world outside this container
EXPOSE 8765

# Define environment variable

# Run app.py when the container launches
CMD ["python", "main.py"]