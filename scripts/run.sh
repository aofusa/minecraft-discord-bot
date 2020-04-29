#! sh

# GCPでマイクラサーバ起動

# GCPの設定読み込み
source ../.env

# インスタンスの起動
gcloud compute instances start $TARGET --zone asia-northeast2-a

# IPアドレスの取得
IP=$(gcloud compute instances list --filter="name=($TARGET)" | tail -n 1 | awk '{print $(NF-1)}')

# DNSにレコードを追加
## GCPに追加
# gcloud dns record-sets transaction start --zone $ZONE
# gcloud dns record-sets transaction add --name $NAME --ttl $TTL --type A $IP --zone $ZONE
# gcloud dns record-sets transaction execute --zone $ZONE || gcloud dns record-sets transaction abort --zone $ZONE

## Cloudflareに追加
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" -H "X-Auth-Email: ${AUTH_EMAIL}" -H "X-Auth-Key: ${AUTH_KEY}" -H "Content-Type: application/json" --data "{\"type\":\"A\",\"name\":\"${DNS_NAME}\",\"content\":\"${IP}\",\"ttl\":120,\"priority\":10,\"proxied\":false}"

# IPアドレスを表示する
echo "Minecraft Server: ${NAME} (${IP}) :25565"

