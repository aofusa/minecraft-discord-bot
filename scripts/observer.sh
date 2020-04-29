#! /bin/bash

MCS=$(sudo screen -ls | grep 'mcs' | wc -l)

# サーバが落ちてたら Java を起動する
if [ ${MCS} -eq 0 ]; then
    echo "[$(date)] minecraft server is down. restart now."
    sudo screen -d -m -S mcs java -Xms1G -Xmx3G -d64 -jar server.jar nogui
    exit
fi

PLAYERS=$(sudo screen -r -X stuff '/list\n' && sleep 5 && cat /home/minecraft/logs/latest.log | grep 'players online:' | tail -n 1 | awk '{print $6}')

echo "[$(date)] online ${PLAYERS}"

# 接続数が 0人なら シャットダウンする
if [ ${PLAYERS} -eq 0 ]; then
    echo "[$(date)] shutdown minecraft server."

    # 設定読み込み
    source ../.env

    ## Cloudflareから削除
    DNS_RECORD=$(curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records?type=A&name=${DNS_NAME}&page=1&per_page=20&order=type&direction=desc&match=all" -H "X-Auth-Email: ${AUTH_EMAIL}" -H "X-Auth-Key: ${AUTH_KEY}" -H "Content-Type: application/json" | jq -r .result[0].id)

    curl -X DELETE "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records/${DNS_RECORD}" -H "X-Auth-Email: ${AUTH_EMAIL}" -H "X-Auth-Key: ${AUTH_KEY}" -H "Content-Type: application/json"

    # インスタンスを停止
    sudo screen -r mcs -X stuff '/stop\n'
    sleep 60
    sudo shutdown
fi
