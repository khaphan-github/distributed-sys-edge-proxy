docker build -f Dockerfile -t envoyrproxy:latest .
minikube image load envoyrproxy:latest
cd k8s
kubectl apply -f deployment-svc.yaml
kubectl get deployment
kubectl get svc
kubectl logs -l app=envoyrproxy --all-containers