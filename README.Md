# Distributed System — Edge Proxy (Envoy + Kubernetes)

A skeleton distributed system demonstrating **Envoy as an edge/sidecar proxy** for service-to-service communication on Kubernetes.

## Why this pattern?

| Problem                                         | Solution via Envoy                                |
| ----------------------------------------------- | ------------------------------------------------- |
| Retry / circuit breaker logic scattered in code | Moved to Envoy proxy layer                        |
| No unified network observability                | Centralized access logs & metrics via Envoy admin |
| Plain HTTP between services                     | TLS termination at proxy level                    |
| Load balancing manually coded                   | ROUND_ROBIN via Envoy cluster config              |

## Architecture

![Architecture](imgs/architechture.png)

```
Client → envoyrproxy-service (LB) → Envoy sidecar → Flask app (ClusterIP)
                                          ↓
                              envoyrproxy-service-app-b → app-b
                              envoyrproxy-service-app-c → app-c
```

> Reference: https://medium.com/@viggnah/how-to-deploy-envoy-as-an-edge-proxy-on-kubernetes-f1af78e1ebfb

---

## Requirements

- Docker
- [minikube](https://minikube.sigs.k8s.io/) (local Kubernetes)
- kubectl

---

## Quick Start

### 1. Install minikube

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
minikube start
```

### 2. Build & load all images

```bash
cd cluster

# Build app images
docker build -f app-a/dockerfile -t edge_proxy_app-a:latest ./app-a
docker build -f app-b/dockerfile -t edge_proxy_app-b:latest ./app-b
docker build -f app-c/dockerfile -t edge_proxy_app-c:latest ./app-c

# Build envoy image
docker build -f envoy/Dockerfile -t edge_proxy_envoy:latest ./envoy

# Load into minikube
minikube image load edge_proxy_app-a:latest
minikube image load edge_proxy_app-b:latest
minikube image load edge_proxy_app-c:latest
minikube image load edge_proxy_envoy:latest
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f app-a/k8s/deployment.yaml
kubectl apply -f app-b/k8s/deployment.yaml
kubectl apply -f app-c/k8s/deployment.yaml
```

### 4. Verify deployments

```bash
kubectl get deployments
kubectl get svc
kubectl get pods
```

---

## Redeploying after code changes

> Use this workflow every time you change app code.

```bash
# 1. Rebuild image (e.g. app-a)
docker build -f app-a/dockerfile -t edge_proxy_app-a:latest ./app-a

# 2. Remove stale image from minikube and reload
minikube ssh "docker rmi -f edge_proxy_app-a:latest"
minikube image load edge_proxy_app-a:latest

# 3. Restart pods to pick up new image
kubectl delete pods -l app=app-a

# 4. Verify rollout
kubectl rollout status deployment app-a-deployment
```

---

## Useful Commands

```bash
# View logs for a service
kubectl logs -l app=app-a --all-containers --follow

# View envoy access logs
kubectl logs -l app=envoyrproxy-app-a --follow

# Check env vars in a running pod
kubectl exec -it $(kubectl get pod -l app=app-a -o jsonpath='{.items[0].metadata.name}') -- env | grep SERVICE

# Describe a deployment
kubectl describe deployment app-a-deployment

# Get minikube service URL
minikube service envoyrproxy-service-app-a --url
```

---

## Port Mapping

| Resource     | app-a                | app-b                | app-c                |
| ------------ | -------------------- | -------------------- | -------------------- |
| ConfigMap    | `envoy-config-app-a` | `envoy-config-app-b` | `envoy-config-app-c` |
| Admin port   | `9901`               | `9902`               | `9903`               |
| Flask port   | `9001`               | `9002`               | `9003`               |
| Service port | `9101`               | `9102`               | `9103`               |
| LB port      | `9210`               | `9220`               | `9230`               |
| Image        | `edge_proxy_app-a`   | `edge_proxy_app-b`   | `edge_proxy_app-c`   |

---

## API Endpoints (app-a)

| Method | Path                | Description                   |
| ------ | ------------------- | ----------------------------- |
| GET    | `/ping`             | Health check                  |
| GET    | `/info`             | Service info & version        |
| POST   | `/explore/services` | Call app-b or app-c via envoy |

**POST `/explore/services` body:**

```json
{ "service": "app:b" }
```

Swagger UI available at: `http://<minikube-ip>:<LB-port>/docs`

---

## Service-to-Service Call Flow

```
app-a  →  envoyrproxy-service-app-b:9220  →  app-b-service:9102  →  app-b pod
app-a  →  envoyrproxy-service-app-c:9230  →  app-c-service:9103  →  app-c pod
```
