# gitops-lumieres

Repo GitOps pour le déploiement de la **todo-api** et du **game-2048** via ArgoCD sur un cluster Kubernetes local (k3d).

---

## Architecture

```
gitops-lumieres/
├── apps/
│     ├── base/                        # Manifests K8s de base (Kustomize)
│     │   ├── todos-api/               # Deployment + Service de la todo-api
│     │   └── game-2048/               # Deployment + Service + Ingress + Namespace
│     └── overlays/
│         ├── dev/                     # Env dev : 1 replica + game-2048
│         └── prod/                    # Env prod : 3 replicas
├── apps-code/
│   └── docker-2048/                     # Code source + Dockerfile du jeu 2048
├── argocd/
│   └── applications/                   # Application CRDs ArgoCD
│       ├── argo-dev.yaml               # App dev → namespace todo-api-dev
│       └── argo-prod.yaml              # App prod → namespace todo-api-prod
└── todo-api-python/                    # Code source de la todo-api (FastAPI)
```

---

## Applications déployées

| App | Image | Dev | Prod |
|-----|-------|-----|------|
| todo-api | `adame555/todo-api:v1.0.0` | 1 replica | 3 replicas |
| game-2048 | `adame555/docker-2048:v3` | oui | non |

---

## Prérequis

- [k3d](https://k3d.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/) (optionnel)

---

## Lancer depuis zéro

### 1. Créer le cluster

```bash
k3d cluster create gitops-lab
```

### 2. Installer ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=180s
```

### 3. Déployer les Applications ArgoCD

```bash
kubectl apply -f argocd/applications/argo-dev.yaml
kubectl apply -f argocd/applications/argo-prod.yaml
```

ArgoCD synchronise automatiquement depuis ce repo Git et déploie les ressources dans les namespaces correspondants.

---

## Accéder aux services

### UI ArgoCD

```bash
# Récupérer le mot de passe admin
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# Exposer l'UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Ouvre **https://localhost:8080** (login: `admin`)

### todo-api (dev)

```bash
kubectl port-forward svc/todo-api -n todo-api-dev 8000:80
```

Endpoints disponibles :
- `GET  http://localhost:8000/todos/`
- `POST http://localhost:8000/todos/`
- `GET  http://localhost:8000/health`

### game-2048 (dev uniquement)

```bash
kubectl port-forward svc/game-2048 -n game-2048 8082:80
```

Ouvre **http://localhost:8082**

---

## Choix techniques

### Kustomize plutôt que Helm

Kustomize permet de séparer clairement la configuration de base des surcharges par environnement sans templating complexe. Chaque overlay (`dev`/`prod`) patche uniquement ce qui diffère (replicas, namespace).

### game-2048 uniquement en dev

Le jeu 2048 est une app de démonstration incluse dans l'overlay `dev` pour tester le déploiement multi-app. Quand elle sera validée, il suffira d'ajouter `../../base/game-2048` dans `overlays/prod/kustomization.yaml`.

### Un seul cluster, deux namespaces

- `todo-api-dev` → environnement de développement (1 replica)
- `todo-api-prod` → environnement de production (3 replicas)
- `game-2048` → namespace dédié au jeu

---

## Environnements

| Namespace | App | Replicas | Géré par |
|-----------|-----|----------|----------|
| `todo-api-dev` | todo-api | 1 | ArgoCD app `dev` |
| `todo-api-prod` | todo-api | 3 | ArgoCD app `prod` |
| `game-2048` | game-2048 | 2 | ArgoCD app `dev` |
