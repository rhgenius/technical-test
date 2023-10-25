APPLICATION
===========

To create a simple HTTP REST application that limits the number of requests based on a source IP address and allows for dynamic rate limiting configuration, we can use Python with the Flask web framework. We'll also utilize a popular rate limiting library called "flask-limiter" to handle the rate limiting logic.

Here's a step-by-step guide to create the application:

1. Install the required Python libraries:

   You'll need Flask and flask-limiter. You can install these libraries using pip:

   ```bash
   pip install flask flask-limiter
   ```

2. Create the Python application:

   Here's a sample Python code for a basic REST application with rate limiting based on the source IP address:

   ```python
   from flask import Flask, request, jsonify
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   app = Flask(__name__)

   # Configure the limiter
   limiter = Limiter(
       app,
       key_func=get_remote_address,  # Rate limiting based on source IP address
       storage_uri="memory://",     # Use in-memory storage (can be replaced with Redis)
       application_limits=["100 per day", "10 per hour"]  # Define rate limits
   )

   @app.route('/api/resource', methods=['GET'])
   @limiter.limit("10 per minute")  # Per-minute rate limit for this endpoint
   def get_resource():
       return jsonify({"message": "Resource accessed successfully"})

   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. Run the application:

   Save the above code to a Python file (e.g., `app.py`). Then, run the application using the following command:

   ```bash
   python app.py
   ```

   Your REST API will be available at `http://localhost:5000/api/resource`.

4. Test the API:

   You can use tools like `curl` or Postman to test the API:

   - Access the resource endpoint (`http://localhost:5000/api/resource`) to make GET requests.
   - The rate limits are configured in the code. In this example, you have a rate limit of 10 requests per minute for the `/api/resource` endpoint. You can change the rate limits without modifying the code by updating the `@limiter.limit` decorator and `application_limits` list.

5. Dynamic rate limiting configuration:

   To allow dynamic rate limiting configuration, you can implement an admin API or a configuration file that can be modified to change the rate limits without stopping the application. You would modify the `application_limits` list based on the new configuration.

This simple Python Flask application provides a basic example of how to create an HTTP REST API with rate limiting based on source IP addresses, and it can be extended to allow for dynamic rate limit configuration based on your specific requirements.

DOCKERFILE
==========

To package the Flask application with rate limiting in a Docker container, you'll need to create a Dockerfile. Here's a simple Dockerfile for your Python application:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

Here's what this Dockerfile does:

1. It uses the official Python 3.8 image as the base image.

2. It sets the working directory to `/app` in the container.

3. It copies the application files from the host machine to the container.

4. It installs any required Python packages defined in `requirements.txt`. You should create a `requirements.txt` file in the same directory as your application code and list the dependencies.

5. It exposes port 80 to allow external access. Note that you can change the port number to the one you use in your Flask application.

6. It defines an environment variable (not used in the example code).

7. Finally, it runs the `app.py` script to start your Flask application.

To build and run the Docker container:

1. Make sure you have Docker installed on your machine.

2. Open a terminal and navigate to the directory where your Dockerfile and application code are located.

3. Build the Docker image by running the following command, replacing `tech-test` with a suitable name for your image:

   ```bash
   docker build -t tech-test .
   ```

4. Once the image is built, you can run a container from it with:

   ```bash
   docker run -p 4000:80 tech-test
   ```

   In this example, the application inside the container listens on port 80, and it's mapped to port 4000 on your host machine.

Your Flask application should now be running inside a Docker container and accessible at `http://localhost:4000/api/resource`.

DOCKER COMPOSE
==============

To create a Docker Compose manifest that can run your application container and add a separate container for forwarding logs to a third-party service like Kibana, you can use the following `docker-compose.yml` file:

```yaml
version: '3'
services:
  app:
    image: tech-test:latest # Replace with the image name you used when building your Flask application
    ports:
      - "4000:80"  # Map the Flask app's port to the host machine

  log_forwarder:
    image: log_forwarder_image:latest  # Replace with the image for your log forwarder
    volumes:
      - ./log_files:/logs  # Mount the directory with log files
    environment:
      - LOG_SOURCE=/logs
      - KIBANA_HOST=kibana-service  # Change this to the address of your Kibana service

# Define a network to allow the containers to communicate
networks:
  default:
    external:
      name: my_network  # Change this to an existing network name or create a new one
```

Here's what this `docker-compose.yml` file does:

- It defines two services: `app` and `log_forwarder`.

- The `app` service runs your Flask application, exposing it on port 4000. Replace `tech-test:latest` with the name of the Docker image you built for your Flask application.

- The `log_forwarder` service runs the log forwarding container. You should replace `log_forwarder_image:latest` with the name of the Docker image you plan to use for log forwarding to Kibana.

- It mounts a volume for log files from the host machine to the log forwarding container. This allows the log forwarder to access the logs generated by your Flask application.

- Environment variables are provided to configure the log forwarder. In this example, `LOG_SOURCE` specifies the source directory for logs, and `KIBANA_HOST` is set to the hostname of your Kibana service.

- A network named `my_network` is defined in the `networks` section. You should change the network name to an existing network if you have one or create a new network.

After creating this `docker-compose.yml` file, you can deploy the application and log forwarder together using the `docker-compose up` command:

```bash
docker-compose up
```

This will start both the Flask application and the log forwarding container. Make sure to replace the placeholders with actual image names and network information relevant to your setup.

CLOUD RUN (BONUS)
=================

To deploy your Flask application on Google Cloud Run, follow these steps:

1. **Prerequisites**:

   - Ensure you have a Google Cloud Platform (GCP) account and have the Google Cloud SDK (gcloud) installed.
   - Make sure you have Docker installed locally.

2. **Containerize Your Application**:

   First, you need to containerize your Flask application as previously discussed by creating a Docker image.

   - Navigate to the directory containing your application code and the Dockerfile.
   - Build the Docker image:

     ```bash
     docker build -t tech-test .
     ```

   - Tag the Docker image for the Google Container Registry:

     ```bash
     docker tag tech-test gcr.io/your-project-id/tech-test:latest
     ```

   Replace `your-project-id` with your GCP project ID.

3. **Push the Docker Image to Google Container Registry**:

   Push the Docker image to the Google Container Registry:

   ```bash
   gcloud auth configure-docker
   docker push gcr.io/your-project-id/tech-test:latest
   ```

4. **Deploy on Cloud Run**:

   Use the following command to deploy your application on Google Cloud Run:

   ```bash
   gcloud run deploy tech-test \
     --image gcr.io/your-project-id/tech-test:latest \
     --platform managed
   ```

   Replace `your-project-id` with your GCP project ID. Follow the prompts to choose the region, allow unauthenticated access (if needed), and confirm the deployment.

5. **Access Your Application**:

   Once the deployment is complete, you will receive a URL for your Cloud Run service. You can access your Flask application via this URL.

6. **(Optional) Configure Rate Limiting**:

   If you want to configure rate limiting, you can use the environment variables for your Flask application within the Cloud Run service. You can set environment variables for your Cloud Run service in the Google Cloud Console under "Cloud Run" -> "Services" -> "tech-test" -> "Edit & Deploy" -> "Variables."

7. **Monitor Logs**:

   Google Cloud Run automatically logs the application's output. You can view these logs in the Google Cloud Console under "Cloud Run" -> "Services" -> "tech-test" -> "Logs."

Your Flask application should now be deployed on Google Cloud Run. Remember to replace `your-project-id` with your actual GCP project ID and make any additional configurations you need, such as rate limiting or other environment variables.
