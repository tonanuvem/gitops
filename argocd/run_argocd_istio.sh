# https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#istio
# curl -kLs -o install.yaml https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

##########

# Aguardando o IP Externo
echo ""
echo "Aguardando o IP Externo do Gateway (Ingress)"
while [ $(kubectl get service istio-ingressgateway -n istio-system -o jsonpath='{ .status.loadBalancer.ingress[].ip }'| wc -m) = '0' ]; do { printf .; sleep 1; } done
export INGRESS_DOMAIN=$(kubectl get service istio-ingressgateway -n istio-system -o jsonpath='{ .status.loadBalancer.ingress[].ip }').nip.io
echo ""
echo "INGRESS_DOMAIN = $INGRESS_DOMAIN"


kubectl label namespace argocd istio-injection=enabled

##########

kubectl create namespace argocd

kubectl apply -k ./ -n argocd --wait=true

openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout private.key \
  -out certificate.crt \
  -days 365 \
  -subj "/CN=argocd.meudominio.com" \
  -addext "subjectAltName = DNS:argocd.meudominio.com"

kubectl create secret tls argocd-server-tls \
  --cert=certificate.crt \
  --key=private.key \
  -n argocd

kubectl apply -f ./istiogateway.yml -n argocd

##########

echo ""
echo "Aguardando a execução da Solução"
while [ $(kubectl get pod -n argocd | grep Running | wc -l) != '7' ]; do { printf .; sleep 1; } done
echo ""
echo "Acessar Demo: https://$INGRESS_DOMAIN/argocd"
echo ""
# kubectl port-forward svc/argocd-server -n argocd 8080:443 &
# Obtenha a senha inicial do admin
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo "Senha do Argo CD: $ARGOCD_PASSWORD"
echo ""
echo ""