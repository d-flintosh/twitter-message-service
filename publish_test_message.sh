TOPIC_ID="projects/sports-data-service/topics/twitter-message-service-pubsub"

gcloud pubsub topics publish ${TOPIC_ID} --message="SEND IT!!!!"