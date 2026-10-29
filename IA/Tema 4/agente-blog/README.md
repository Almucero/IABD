# Agente y herramientas del blog

Ejecuta estos comandos en PowerShell desde la carpeta `agente-blog`.

## Preparación

Instala las dependencias y descarga los modelos usados:

```powershell
uv sync
ollama pull qwen3.5:9b
ollama pull qwen3.8:27b
```

Inicia el servidor web del blog en otra terminal:

```powershell
Set-Location ..\blog
.\.venv\Scripts\Activate.ps1
python src\manage.py runserver
```

Para crear borradores, copia `.env.example` como `.env`, pega un token de
administrador del blog tras `BLOG_API_TOKEN=` y cárgalo en la terminal de
`agente-blog`:

```powershell
Copy-Item .env.example .env
$env:BLOG_API_TOKEN = ((Get-Content .env | Where-Object { $_ -like 'BLOG_API_TOKEN=*' } | Select-Object -First 1) -replace '^BLOG_API_TOKEN=', '').Trim()
```

Consulta cómo obtener el token en el
[README del blog](../blog/README.md#token-y-pruebas-de-la-api).

## Ejecutar

| Archivo | Comando | Requisitos |
|---|---|---|
| [`agente.py`](agente.py) | `uv run python agente.py` | Ollama y servidor del blog; token para guardar borradores |
| [`prueba_herramientas.py`](prueba_herramientas.py) | `uv run python prueba_herramientas.py` | Servidor del blog y token; crea un borrador |
| [`servidor_mcp.py`](servidor_mcp.py) | `uv run mcp run servidor_mcp.py --transport streamable-http` | Servidor del blog; token para crear borradores |
| [`prueba_mcp.py`](prueba_mcp.py) | `uv run python prueba_mcp.py` | Servidor MCP en ejecución |
| [`agente_con_mcp.py`](agente_con_mcp.py) | `uv run python agente_con_mcp.py` | Ollama, servidor MCP y token; crea un borrador |
| [`prueba_tool_calling.py`](prueba_tool_calling.py) | `uv run python prueba_tool_calling.py` | Ollama |

El servidor MCP escucha en `http://127.0.0.1:8001/mcp`. Mantén abierta su
terminal mientras ejecutes `prueba_mcp.py` o `agente_con_mcp.py`. Ollama usa
`qwen3.5:9b` en los agentes y `qwen3.8:27b` en `prueba_tool_calling.py`.
