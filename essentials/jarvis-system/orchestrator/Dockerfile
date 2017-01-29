# Use hypriot python image
FROM hypriot/rpi-python

# Set workdir
WORKDIR /usr/src/app

# COPY everything
COPY . /usr/src/app

# Expose 8080 port
EXPOSE 8080

# Install gcc required for gevents
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Run pip install
RUN pip install -r /usr/src/app/requirements.txt

# Clean up gcc and other installs
RUN apt-get purge -y --auto-remove gcc

# Run app
CMD ["python", "/usr/src/app/src/server.py"]
