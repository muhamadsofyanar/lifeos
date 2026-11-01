FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 DATA_DIR=/data PORT=8000 COOKIE_SECURE=true
WORKDIR /app
RUN groupadd -g 10001 lifeos && useradd -u 10001 -g lifeos -M lifeos && mkdir /data && chown lifeos:lifeos /data
COPY --chown=lifeos:lifeos server.py /app/server.py
COPY --chown=lifeos:lifeos static /app/static
USER lifeos
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"
CMD ["python", "server.py"]
