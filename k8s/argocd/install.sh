# 네임스페이스 생성
kubectl create namespace argocd

# 메니페스트 다운로드
curl -O https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
sudo mv install.yaml argocd.yaml

# 설치
kubectl apply -f argocd.yaml -n argocd

# 초기 비밀번호 확인
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode; echo