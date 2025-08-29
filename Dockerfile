# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY grafana_helper.py .

# Make port 80 available to the world outside this container
# (Not strictly necessary for this script, but good practice if it were a web service)
# EXPOSE 80

# Define environment variables (optional, can be passed at runtime)
# ENV GRAFANA_URL="http://localhost:3000"
# ENV GRAFANA_API_KEY=""

# Run grafana_helper.py when the container launches
ENTRYPOINT ["python3", "grafana_helper.py"]

# Default command can be provided here, e.g. --help
# CMD ["--help"]
