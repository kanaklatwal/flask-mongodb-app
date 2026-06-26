# Flask + MongoDB Deployment on Kubernetes

## Project Overview

This project demonstrates the deployment of a Python Flask application with MongoDB on a Kubernetes cluster using Minikube.

The Flask application provides two endpoints:

* `/` – Displays a welcome message with the current date and time.
* `/data` – Stores and retrieves data from MongoDB.

MongoDB is deployed as a StatefulSet with persistent storage and authentication enabled. The Flask application is deployed with multiple replicas and exposed using a Kubernetes Service.

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

```bash
docker build -t flask-mongodb-app:v1 .
```

---

# Load Image into Minikube

```bash
minikube image load flask-mongodb-app:v1
```

---

# Deploy Kubernetes Resources

```bash
kubectl apply -f k8s/
```

Verify the deployment:

```bash
kubectl get all
```

---

# Access the Application

Run the following command:

```bash
minikube service flask-service --url
```

This command generates a local URL.

Example:

```
http://127.0.0.1:56829
```

Open the generated URL in your browser.

---

# Kubernetes Resources

The following Kubernetes resources were created:

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

Kubernetes automatically provides DNS for Services.

The Flask application connects to MongoDB using the MongoDB Service name instead of the Pod IP.

Example:

```
mongodb-service:27017
```

Even if the MongoDB Pod is recreated, the Service name remains the same, so the Flask application can continue communicating with the database without any configuration changes.

---

# Resource Requests and Limits

Resource Requests reserve the minimum CPU and memory required by a container.

Resource Limits define the maximum CPU and memory a container can use.

Configuration used:

| Resource | Request | Limit |
| -------- | ------- | ----- |
| CPU      | 200m    | 500m  |
| Memory   | 250Mi   | 500Mi |

These values help in efficient resource utilization and prevent a single container from consuming excessive cluster resources.

---

# Design Choices

* MongoDB is deployed as a StatefulSet because database applications require stable storage.
* Persistent Volume and Persistent Volume Claim are used to retain database data after Pod restarts.
* Flask is deployed using a Deployment with two replicas to improve availability.
* MongoDB is exposed using a ClusterIP Service because it only needs to communicate within the cluster.
* Flask is exposed using a NodePort Service so that it can be accessed from the local machine.
* Horizontal Pod Autoscaler is configured for automatic scaling based on CPU utilization.

---

# Testing

The following checks were performed during testing:

* Docker image built successfully.
* Docker image loaded into Minikube.
* Kubernetes resources deployed successfully.
* MongoDB Pod started successfully.
* Flask Deployment started with two running Pods.
* Flask application connected successfully to MongoDB.
* Application was accessible using the Minikube service URL.
* Kubernetes resources were verified using `kubectl get all`.

---

# Commands Used

```bash
docker build -t flask-mongodb-app:v1 .

minikube image load flask-mongodb-app:v1

kubectl apply -f k8s/

kubectl get all

kubectl get pods

kubectl get svc

minikube service flask-service --url
```

---

# Output

* Flask Deployment: Running (2/2)
* MongoDB StatefulSet: Running (1/1)
* Services: Running
* HPA: Created
* Application accessible through browser using the Minikube service URL.
