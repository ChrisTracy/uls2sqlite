FROM ubuntu:latest

# Install git, Python 3, unzip, curl, sqlite-utils, and GNU Parallel
RUN apt-get update && \
    apt-get install -y git python3 unzip curl nano && \
    apt-get install -y python3-pip && \
    pip3 install sqlite-utils && \
    apt-get install -y parallel

# Set the working directory
WORKDIR /app

# Clone the scripts from GitHub
RUN git clone https://github.com/ChrisTracy/uls2sqlite .

# Make all scripts executable
RUN find . -type f -name "*.sh" -exec chmod +x {} \;

# Define the command to run when the container starts
CMD ["./download_weekly_dbs.sh"]