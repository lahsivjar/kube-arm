# Use hypriot python image
FROM hypriot/rpi-python

# Set workdir
WORKDIR /usr/src/app

# COPY everything
COPY . /usr/src/app

# Expose 8080 port
EXPOSE 8080

# Run pip install
RUN pip install -r /usr/src/app/requirements.txt

# Run app
CMD ["python", "/usr/src/app/src/server.py"]
