FROM python:3.7-slim AS build-env
ADD src /app
ADD requirements.txt /app
WORKDIR /app
RUN pip install --target=/app --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian10
COPY --from=build-env /app /app
WORKDIR /app

# GCP
ENV GOOGLE_APPLICATION_CREDENTIALS your-credentials-path
ENV TARGET your-instance
ENV ZONE your-zone
ENV NAME your-domain-mane
ENV PROJECT your-project
ENV GCP_ZONE your-gcp-zone
ENV TTL 21600

# Cloudflare
ENV DOMAIN your-domain
ENV AUTH_EMAIL your-email
ENV AUTH_KEY your-auth-key
ENV ZONE_ID your-zone-id
ENV DNS_NAME your-domain-name

# Discord
ENV DISCORD_WEBHOOK your-discord-webhook
ENV DISCORD_TOKEN your-discord-token

CMD ["bot.py"]