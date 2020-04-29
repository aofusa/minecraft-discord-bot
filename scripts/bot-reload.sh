#! /bin/bash

if [ -f ~/.bash_profile ]; then
    source ~/.bash_profile
fi

# Get this scripts path and move .. path
(cd $(cd $(dirname $0); pwd)/.. && \

# Rebuild and apply k8s Cluster
docker build -t dev.local/ours-minecraft-service-bot . \
&& kubectl apply -k . \
&& kubectl delete -f deploy-bot.yaml \
&& kubectl apply -f deploy-bot.yaml)

