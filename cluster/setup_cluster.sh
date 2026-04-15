#!/usr/bin/env bash

minikube image load edge_proxy_app-a:latest
minikube image load edge_proxy_app-b:latest
minikube image load edge_proxy_app-c:latest
minikube image load edge_proxy_envoy:latest

minikube image ls

# Deploy service
kubectl apply -f app-a/k8s/deployment-svc.yaml
kubectl apply -f app-a/k8s/configmap-envoy.yaml
kubectl apply -f app-a/k8s/deployment-envoy-app.yaml


kubectl apply -f app-b/k8s/deployment-svc.yaml
kubectl apply -f app-b/k8s/configmap-envoy.yaml
kubectl apply -f app-b/k8s/deployment-envoy-app.yaml

kubectl apply -f app-c/k8s/deployment-svc.yaml
kubectl apply -f app-c/k8s/configmap-envoy.yaml
kubectl apply -f app-c/k8s/deployment-envoy-app.yaml

kubectl get svc
#