FROM apify/actor-node:16

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Set Python aliases
RUN ln -sf python3 /usr/bin/python && \
    ln -sf pip3 /usr/bin/pip

# Copy package files
COPY package.json ./
COPY requirements.txt ./

# Install Node.js dependencies
RUN npm install

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Run the actor
CMD ["node", "main.js"] 