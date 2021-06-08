
function enable_service() {
  service=$1
  echo "Enabling ${service}"
  gcloud services enable ${service} || echo "NoOP"
}

enable_service "secretmanager.googleapis.com"

#gcloud secrets create twitter-automation-001
#gcloud secrets versions add twitter-automation-001 --data-file="path-to-secrets"

