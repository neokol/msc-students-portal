# Academic Portal Application

## Overview

This application provides a platform for managing student grades. Professors can enter grades, secretaries can confirm and finalize them, and students can view their detailed scores.

## Prerequisites

- Docker
- Kubernetes (e.g., Minikube, MicroK8s, or a managed Kubernetes service)
- kubectl configured to interact with your Kubernetes cluster
- Access to a container registry (e.g., GitHub Packages)
- Node.js and npm (for building the frontend)

## Installation Steps

### Install Kubernetes

#### Installing MicroK8s

MicroK8s is a lightweight Kubernetes distribution that runs on various platforms. Below are the steps to install MicroK8s on different operating systems.

Open a terminal and run the following commands:

```bash
sudo snap install microk8s --classic
```

Add Your User to the microk8s Group

```bash
sudo usermod -a -G microk8s <your_username>
sudo chown -f -R <your_username> ~/.kube
```

MicroK8s comes with several useful add-ons that can be enabled based on your needs. For example:

```bash
microk8s enable dns dashboard storage
```

Access Kubernetes Commands

To access the Kubernetes command-line tool (kubectl), use:

```bash
microk8s kubectl get nodes
```

This command should show the nodes in your MicroK8s cluster.

#### Cloning Your GitHub Repository

1. Navigate to Desired Directory

```bash
cd path/to/your/desired/directory
```

2. Clone the Repository

```bash
git clone https://github.com/neokol/msc-students-portal.git
```

3. Find k8s directory

```bash
cd /k8s
```

#### Deployment

1. Apply Namespace

```bash
kubectl create namespace students-grades-portal
```

2. Apply Deployment and Service YAMLs

```bash
kubectl apply -f *.yaml --namespace=students-grades-portal
```

3. Verify Deployment

```bash
kubectl get all --namespace=students-grades-portal
```
