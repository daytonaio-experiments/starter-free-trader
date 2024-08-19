# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Set the default command to python3
CMD ["python3"]