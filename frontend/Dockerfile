# Use the official Node.js image as a base
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock to install dependencies
COPY package.json yarn.lock /app/

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY . /app/

# Expose port 3000 to access the application
EXPOSE 3000

# Start the application
CMD ["yarn", "start"]
