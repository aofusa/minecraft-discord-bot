マイクラサーバ
---


マイクラサーバ  


## 使い方

```sh
# 起動
run.sh

# 停止
shutdown.sh
```


## TODO

- 現在接続人数の取得 Ok

- 接続人数の定期監視 Ok
  - cron とか

- 接続人数が0人で一定時間 -> インスタンス停止(shutdown.shの実行) Ok

- Discord bot から 起動 と 停止 Ok
  - run.sh と shutdown.sh の python スクリプト化 Ok
  - template.conf の GCP シークレット化 Ok


## 作成手順

https://cloud.google.com/solutions/gaming/minecraft-server?hl=ja


## 上記作成手順+α

- startup_script を下記の通り修正  
```sh
#!/bin/bash
mount /dev/disk/by-id/google-minecraft-disk-1 /home/minecraft
(crontab -l | grep -v -F "/home/minecraft/backup.sh" ; echo "0 */4 * * * /home/minecraft/backup.sh")| crontab -
cd /home/minecraft
at -f register-observer.sh now +10 minutes
screen -d -m -S mcs java -Xms1G -Xmx3G -d64 -jar server.jar nogui
```

- 下記 2スクリプトを /home/minecraft 直下に配置  
  - scripts/observer.sh  
  - scripts/register-observer.sh  
    - source ../.env となっている箇所は正しい内容に修正する  

- 下記 環境変数の情報を /home/minecraft 直下に配置  
  - .env


## そのほか注意点

DNS に Cloudflare を使っているので、それようにスクリプトを作成しています。  
GCP の DNS サービスを使う場合はそれようにコードを修正する必要があります。  

DNS サービスは使わず、IPアドレスをそのまま使用する場合は関係ないです。  

