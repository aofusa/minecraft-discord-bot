#! /bin/bash

# GCPでマイクラサーバをサーバごとダウン

# 設定読み込み
source ../.env

# IPアドレスの取得
IP=$(gcloud compute instances list --filter="name=($TARGET)" | tail -n 1 | awk '{print $5(NF-1);}')

# DNSからレコードを削除
## GCPから削除
# gcloud dns record-sets transaction start --zone $ZONE
# gcloud dns record-sets transaction remove --zone $ZONE --name $NAME --ttl $TTL --type A $IP
# gcloud dns record-sets transaction execute --zone $ZONE || gcloud dns record-sets transaction abort --zone $ZONE

## Cloudflareから削除
DNS_RECORD=$(curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records?type=A&name=${DNS_NAME}&page=1&per_page=20&order=type&direction=desc&match=all" -H "X-Auth-Email: ${AUTH_EMAIL}" -H "X-Auth-Key: ${AUTH_KEY}" -H "Content-Type: application/json" | jq -r .result[0].id)

curl -X DELETE "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records/${DNS_RECORD}" -H "X-Auth-Email: ${AUTH_EMAIL}" -H "X-Auth-Key: ${AUTH_KEY}" -H "Content-Type: application/json"

# インスタンスを停止
gcloud compute instances stop $TARGET --zone asia-northeast2-a

