FROM python:3.12-slim

# Install bash and sudo
RUN apt-get update && apt-get install -y \
    bash \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Make scripts executable
RUN chmod +x setup.sh run.sh

# Run setup script (which uses sudo for espeak install)
RUN ./setup.sh

# Run lesson 1 by default
CMD ["./run.sh", "1"]
