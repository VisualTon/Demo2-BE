# Demo2-BE
## Steps
- [x] Create a cluster by aws eks
- [x] Download kubeconfig to deploy and manage resource
```bash
aws eks update-kubeconfig --name VisualTon2 --region ap-northeast-1
export KUBECONFIG=$KUBECONFIG:/Users/leo_1/.kube/config
```
- [x] Create container by docker and mysql
- [ ] write Kubernetes yaml(deployment.yaml) about container and image
- [ ] Deploy container to cluster by Kubernetes yaml(deployment.yaml)
```bash
# 部署應用程式
kubectl apply -f your-app.yaml

# 查看部署
kubectl get deployments

# 檢查 POD
kubectl get pods
```
- [ ] the container run on the cluster
- [ ] k8s Rolling Updates
## Config
- container name: VTC, image name: mysql:8.0
- cluster name: VisualTon2, region: ap-northeast-1
