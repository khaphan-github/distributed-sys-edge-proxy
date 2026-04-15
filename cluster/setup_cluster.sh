#!/usr/bin/env bash
docker build -t edge_proxy_app-a:v1.0.1 ./app-a

minikube image load edge_proxy_app-a:v1.0.1
minikube image load edge_proxy_app-b:v1.0.1
minikube image load edge_proxy_app-c:v1.0.1
minikube image load edge_proxy_envoy:v1.0.1

minikube image ls

# Deploy service
kubectl apply -f app-a/k8s/deployment.yaml
kubectl apply -f app-b/k8s/deployment.yaml
kubectl apply -f app-c/k8s/deployment.yaml

kubectl get svc
#