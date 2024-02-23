# Kubernetes

## Kustomize

```bash
# Only use kubectl apply -k <dir> for kustomize
kubectl apply -k <dir>

# kustomize
kustomize init
kustomize build . | kubectl apply -f -
kustomize build base
kustomize build .
kustomize edit add resource *.yaml
```

## Basic Application

[Installation - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/)
[Longhorn | Install with ArgoCD](https://longhorn.io/docs/1.6.0/deploy/install/install-with-argocd/)

## Context

```bash
# copy context
kubectl config current-context | xclip -selection clipboard
kubectl config get-contexts
kubectl config use-context <context>

```

## Debugging

[Troubleshooting Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)

```bash
# Pod
kubectl describe pod <pod_name>
kubectl describe rc ${CONTROLLER_NAME}
kubectl get endpoints ${SERVICE_NAME}


```

## Cleaning

```bash
# Pod stuck in Terminating
kubectl delete pod <pod_name> --grace-period=0 --force

# Purge namespace
kubectl delete namespace <namespace>

```
