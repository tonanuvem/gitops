# Aguardando o IP Externo
echo ""
echo "Aguardando o IP Externo do Gateway (Ingress)"
while [ $(kubectl get service istio-ingressgateway -n istio-system -o jsonpath='{ .status.loadBalancer.ingress[].ip }'| wc -m) = '0' ]; do { printf .; sleep 1; } done
export INGRESS_DOMAIN=$(kubectl get service istio-ingressgateway -n istio-system -o jsonpath='{ .status.loadBalancer.ingress[].ip }').nip.io
echo ""
echo "INGRESS_DOMAIN = $INGRESS_DOMAIN"


kubectl label namespace argocd istio-injection=enabled

# Utilizar o objeto Gateway (Ingress) para limitar o uso dos IPs publicos
# https://istio.io/latest/docs/tasks/observability/gateways/#option-2-insecure-access-http

# 1. Apply the following configuration to expose E-COMMERCE:
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: argocd-gateway
  namespace: argocd
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http-argocd
      protocol: HTTP
    hosts:
    - "argocd.${INGRESS_DOMAIN}"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: argocd-vs
  namespace: argocd
spec:
  hosts:
  - "argocd.${INGRESS_DOMAIN}"
  gateways:
  - argocd-gateway
  http:
  - route:
    - destination:
        host: argocd-server
        port:
          number: 80
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: argocd
  namespace: argocd
spec:
  host: argocd-server
  trafficPolicy:
    tls:
      mode: DISABLE
---
EOF

echo ""
echo "Aguardando a execução da Solução"
while [ $(kubectl get pod -n argocd | grep Running | wc -l) != '7' ]; do { printf .; sleep 1; } done
echo ""
echo "Acessar Demo: http://argocd.$INGRESS_DOMAIN"
echo ""
# kubectl port-forward svc/argocd-server -n argocd 8080:443 &
# Obtenha a senha inicial do admin
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo "Senha do Argo CD: $ARGOCD_PASSWORD"
echo ""
echo ""