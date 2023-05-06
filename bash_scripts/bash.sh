#!/bin/bash

# Set the deployment name prefix
DEPLOYMENT_PREFIX="pre-production-extracting-emails-demo-deployment"

# Delete any existing deployments with the prefix
kubectl delete deployments --all

# Loop 3 times to create 3 new deployments
for i in {1..3}; do
  # Generate a unique deployment name using the prefix and a timestamp
  DEPLOYMENT_NAME="${DEPLOYMENT_PREFIX}$(date +%s)"

  # Create the deployment using kubectl
  kubectl create -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${DEPLOYMENT_NAME}
spec:
  replicas: 5
  selector:
    matchLabels:
      app: extracting-emails
  template:
    metadata:
      labels:
        app: extracting-emails
    spec:
      containers:
        - name: extracting-emails-container
          image: kartikeya24/eek8s
          ports:
            - containerPort: 80
          env:
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-access-key
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgresdb-credentials
                  key: postgres-user
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresdb-credentials
                  key: postgres-password
EOF
  sleep 60 # Wait for 1 minute before creating the next deployment
done

# Wait for 5 hours before creating the next set of deployments
sleep 18000 # 5 hours in seconds

# Delete any existing deployments with the prefix
kubectl delete deployments --all