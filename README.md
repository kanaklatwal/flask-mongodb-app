# Flask + MongoDB Deployment on Kubernetes

## Project Overview

This project demonstrates how to deploy a Python Flask application with MongoDB on a Kubernetes cluster using Minikube.
The deployment was verified using Kubernetes resources, browser testing, and Horizontal Pod Autoscaler (HPA) metrics.
The Flask application provides two REST endpoints:

* **/** – Displays a welcome message with the current date and time.
* **/data** – Stores and retrieves data from MongoDB.

MongoDB is deployed as a StatefulSet with authentication enabled and persistent storage. The Flask application is deployed using Kubernetes Deployment with two replicas and exposed using a NodePort Service.

---

# Technologies Used

* Python Flask
* MongoDB
* Docker
* Kubernetes
* Minikube

---

# Project Structure

```text
flask-mongodb-app/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── k8s/
    ├── secret.yaml
    ├── pv.yaml
    ├── pvc.yaml
    ├── mongodb-statefulset.yaml
    ├── mongodb-service.yaml
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    └── hpa.yaml
```

---

# Build Docker Image

Build the Docker image using:

```bash
docker build -t flask-mongodb-app:v1 .
```

---

# Push Docker Image (Container Registry)

If you want to push the Docker image to Docker Hub:

```bash
docker tag flask-mongodb-app:v1 <dockerhub-username>/flask-mongodb-app:v1

docker login

docker push <dockerhub-username>/flask-mongodb-app:v1
```

For this assignment, the image was deployed locally by loading it into Minikube.

```bash
minikube image load flask-mongodb-app:v1
```

---

# Deploy on Minikube

Deploy all Kubernetes resources:

```bash
kubectl apply -f k8s/
```

Verify deployment:

```bash
kubectl get all
```

---

# Access the Application

Run:

```bash
minikube service flask-service --url
```

Example output:

```text
http://127.0.0.1:56829
```

Open the generated URL in your browser.

---

# Kubernetes Resources

The following resources were created:

* Secret
* Persistent Volume (PV)
* Persistent Volume Claim (PVC)
* MongoDB StatefulSet
* MongoDB Service (ClusterIP)
* Flask Deployment (2 Replicas)
* Flask Service (NodePort)
* Horizontal Pod Autoscaler (HPA)

---

# DNS Resolution

Kubernetes automatically assigns a DNS name to every Service.

Instead of connecting to MongoDB using a Pod IP address, the Flask application connects using the Service name:

```text
mongodb-service:27017
```

If the MongoDB Pod restarts or its IP changes, the Service name remains the same. This allows reliable communication between the Flask application and MongoDB.

---

# Resource Requests and Limits

Resource Requests define the minimum CPU and memory reserved for a container.

Resource Limits define the maximum CPU and memory a container is allowed to use.

Configuration used:

| Resource | Request | Limit |
| -------- | ------- | ----- |
| CPU      | 200m    | 500m  |
| Memory   | 250Mi   | 500Mi |

These values help improve cluster stability and prevent a single container from consuming excessive resources.

---

# Design Choices

* Flask was deployed using a Deployment because it is a stateless application and needs multiple replicas.
* MongoDB was deployed using a StatefulSet because databases require stable storage and persistent identities.
* ClusterIP Service was used for MongoDB since it only needs to communicate within the Kubernetes cluster.
* NodePort Service was used for the Flask application so it could be accessed from the local machine.
* Persistent Volume (PV) and Persistent Volume Claim (PVC) were used to preserve MongoDB data after pod restarts.
* Kubernetes Secret was used to store MongoDB credentials securely.
* Horizontal Pod Autoscaler (HPA) was configured to automatically scale the Flask application when CPU utilization increases.

I considered deploying MongoDB using a Deployment, but StatefulSet is more suitable because it provides stable storage and predictable Pod names for database workloads.

---

# Testing Scenarios

### Application Deployment

The following checks were performed:

* Docker image built successfully.
* Docker image loaded into Minikube.
* Kubernetes resources deployed successfully.
* MongoDB StatefulSet started successfully.
* Flask Deployment started with two running Pods.
* Application opened successfully in the browser.
* Flask successfully connected to MongoDB.
* Deployment verified using:

```bash
kubectl get all
```

### Autoscaling

The Horizontal Pod Autoscaler (HPA) was successfully configured and verified.

Verification commands:

```bash
kubectl get hpa
kubectl top pods
```

HPA Configuration:

- Minimum Replicas: 2
- Maximum Replicas: 5
- Target CPU Utilization: 70%

Metrics collected during testing:

| Pod | CPU | Memory |
|-----|-----|--------|
| Flask Pod 1 | 1m | 24Mi |
| Flask Pod 2 | 1m | 24Mi |
| MongoDB Pod | 15m | 389Mi |

The Metrics Server was enabled successfully, allowing CPU and memory usage to be monitored using `kubectl top pods`.

See the screenshots in the `screenshots/` folder for verification.

The HPA was configured with:

* Minimum Replicas: 2
* Maximum Replicas: 5
* Target CPU Utilization: 70%

Since this project was tested on a local Minikube cluster with a light workload, CPU utilization did not exceed the scaling threshold during testing. However, the HPA configuration was verified successfully and is ready to scale the application when CPU usage increases.

### Database Testing

* Verified that MongoDB authentication was working.
* Verified that the Flask application successfully stored and retrieved data from MongoDB.
* Confirmed that database storage remained available after restarting the MongoDB Pod.

### Issues Encountered

During development, a few issues were encountered:

* MongoDB image initially failed with `ImagePullBackOff`.
* The issue was resolved by pulling the image locally and loading it into Minikube using:

```bash
docker pull mongo:latest

minikube image load mongo:latest
```

Another issue was accessing the application through the NodePort. This was resolved by using:

```bash
minikube service flask-service --url
```

---

# Useful Commands

```bash
docker build -t flask-mongodb-app:v1 .

minikube image load flask-mongodb-app:v1

kubectl apply -f k8s/

kubectl get all

kubectl get pods

kubectl get svc

kubectl get hpa

minikube service flask-service --url

kubectl top pods
```

---

# Output

The application was successfully deployed on a Minikube Kubernetes cluster.

* Flask Deployment: Running (2/2)
* MongoDB StatefulSet: Running (1/1)
* Services: Running
* Horizontal Pod Autoscaler: Successfully Configured and Verified
  Metrics Server: Enabled
  CPU and Memory Metrics: Verified using kubectl top pods
* Application accessible through browser using the Minikube service URL.

# Screenshots

The following screenshots are included in the `screenshots/` folder:

| Screenshot | Description |
|------------|-------------|
| flask-home.png | Flask application running in the browser |
| kubectl-get-all.png | Verification of deployed Kubernetes resources |
| hpa.png | Horizontal Pod Autoscaler configuration |
| data-test.png | CPU and memory metrics collected using `kubectl top pods` |