FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
  && rm -rf /var/lib/apt/lists/*
COPY cloud/ /app/cloud/
COPY prospecting/ /app/prospecting/
RUN chmod +x /app/cloud/start.sh && mkdir -p /data
EXPOSE 8080
CMD ["/bin/bash", "/app/cloud/start.sh"]
