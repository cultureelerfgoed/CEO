FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir "mcp[cli]" httpx
COPY ldv_mcp.py .
ENV MCP_TRANSPORT=http MCP_HOST=0.0.0.0 MCP_PORT=8000
ENV LDV_ENDPOINT=https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql
EXPOSE 8000
CMD ["python", "ldv_mcp.py"]
