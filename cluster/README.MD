# Router Chain
## Request Flow Diagram

```mermaid
graph LR
    External["External Request<br/>Port 80"]
    Envoy["Envoy Container<br/>Listen Port 3200"]
    SvcA["Service App-A<br/>Port 4200<br/>Internal IP"]
    AppA["App-A Pod<br/>Forward to Port 5200"]

    External -->|Port 80| Envoy
    Envoy -->|Forward to 4200<br/>Call Internal IP| SvcA
    SvcA -->|Direct Traffic| AppA
    AppA -->|Internal Port 5200| AppLogic["Application Logic"]
```

## Detailed Breakdown

1. **External Request (Port 80)**
   - Client sends request to port 80

2. **Envoy Container (Port 3200)**
   - Envoy listens on port 3200
   - Configured to forward traffic to port 4200 using internal IP

3. **Service App-A (Port 4200)**
   - Kubernetes service listening on port 4200
   - Routes traffic to App-A pods

4. **App-A Pod (Port 5200)**
   - Application receives traffic and processes it on internal port 5200
