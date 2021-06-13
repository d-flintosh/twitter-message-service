PROJECT_ID="sports-data-service"

function enable_service() {
  service=$1
  echo "Enabling ${service}"
  gcloud services enable ${service} || echo "NoOP"
}


enable_service "secretmanager.googleapis.com"

TWITTER_MESSAGE_SERVICE_ACCOUNT="twitter-message-service"

gcloud iam service-accounts create ${TWITTER_MESSAGE_SERVICE_ACCOUNT} \
    --description="Service account for twitter-message-service" \
    --display-name=${TWITTER_MESSAGE_SERVICE_ACCOUNT} || echo "NoOP"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${TWITTER_MESSAGE_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor" || echo "NoOP"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${TWITTER_MESSAGE_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/pubsub.publisher" || echo "NoOP"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${TWITTER_MESSAGE_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer" || echo "NoOP"

gcloud iam roles create collaborator --project=${PROJECT_ID} \
  --file=./collaborator-iam-role.yaml || echo "NoOP"


#gcloud secrets create twitter-automation-001
#gcloud secrets versions add twitter-automation-001 --data-file="path-to-secrets"

#gcloud beta builds triggers create cloud-source-repositories \
#    --repo=d-flintosh/twitter-message-service \
#    --branch-pattern="^master$" \
#    --build-config=./cloud-build.yaml