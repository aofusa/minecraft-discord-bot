Discord Minecraft Bot
=====


Discord から呼び出す minecraft bot  


## 概要

以下の手順で作成されたインスタンスに対して、Discord の Bot 経由で起動したり  
ChatOps 的な操作ができるような Bot を作成する  
https://cloud.google.com/solutions/gaming/minecraft-server?hl=ja  


## Bot の使い方  

- 使い方  
下記のコマンドでサーバの操作が可能  
  - /mcstart  
    - マイクラサーバの起動  
  - /mcstop  
    - マイクラサーバの停止  


- 使用準備  
  1. Bot作って Discord に招待する  
  2. 必要な環境変数を埋めて k8sにデプロイ or ローカルで起動する  


## 環境毎の環境変数を準備

```sh
echo "
# GCP
GOOGLE_APPLICATION_CREDENTIALS=your-credentials-path
TARGET=your-instance
ZONE=your-zone
NAME=your-domain-mane
PROJECT=your-project
GCP_ZONE=your-gcp-zone
TTL=21600

# Cloudflare
DOMAIN=your-domain
AUTH_EMAIL=your-email
AUTH_KEY=your-auth-key
ZONE_ID=your-zone-id
DNS_NAME=your-domain-name

# Discord
DISCORD_WEBHOOK=your-discord-webhook
DISCORD_TOKEN=your-discord-token
" > .env
```

.credentials 配下に GCP のAPIキーのファイルを入れる  
APIキーのファイル名は .credentials/gcp.json にリネームしておくとそのまま使える  
詳しくは下記ドキュメントを参照  
https://cloud.google.com/docs/authentication/production?hl=ja#auth-cloud-implicit-python  



## 開発環境構築

```sh
# 実行環境の構築
pipenv --python 3.7

# 依存関係のインストール
pipenv install --skip-lock

# 依存関係のロック
pipenv run pip freeze > requirements.txt

# 開発環境でのデバッグ実行
pipenv run python src/bot.py
```


## コンテナビルド

```sh
docker build -t dev.local/ours-minecraft-service-bot .
```

```sh
# 実行（一時的な実行）
docker run \
    --rm \
    --env-file=.env \
    dev.local/ours-minecraft-service-bot

# 実行（永続的な実行）
docker run \
    --detach \
    --env-file=.env \
    --restart=always \
    dev.local/ours-minecraft-service-bot
```

## kubernetes クラスターへのデプロイ

```sh
# シークレットの作成
kubectl apply -k .

# デプロイ
kubectl apply -f deploy-bot.yaml

# 確認
kubectl get secrets
kubectl describe secrets/ours-minecraft-service-bot-secret
kubectl describe deployments ours-minecraft-service-bot
kubectl get pods --output=wide --watch
kubectl logs ours-minecraft-service-bot-deployment-86b54f6549-bf95v

# 削除する場合
kubectl delete -f deploy-bot.yaml
kubectl delete -k .
```


## 開発環境への再適用手順

```sh
docker build -t dev.local/ours-minecraft-service-bot . \
&& kubectl apply -k . \
&& kubectl delete -f deploy-bot.yaml \
&& kubectl apply -f deploy-bot.yaml
```


## 最終的にデプロイする場合

- 開発環境のクリーンアップ  
```sh
kubectl delete -f deploy-bot.yaml
kubectl delete -k .
```

- 専用 namespace を作成しデプロイ  
```sh
# Namespace の名前を指定
NAMESPACE=ours-minecraft-service-bot

# Namespace の作成
kubectl create namespace ${NAMESPACE}

# Namespace へデプロイ
kubectl apply -k . --namespace ${NAMESPACE}
kubectl apply -f deploy-bot.yaml --namespace ${NAMESPACE}
```

