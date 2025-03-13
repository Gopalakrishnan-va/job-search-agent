FROM apify/actor-python:3.11

# Copy package files
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Make sure the entrypoint is executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Run the actor
ENTRYPOINT ["python", "-m", "src.main"] 