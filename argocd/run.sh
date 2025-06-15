# Criar o namespace para o Argo CD
kubectl create namespace argocd

# Aplicar o manifesto de instalação oficial
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Instalar a CLI do Argo CD
VERSION=$(curl --silent "https://api.github.com/repos/argoproj/argo-cd/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")')
sudo curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/$VERSION/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd
argocd version --client