"""Servidor MCP"""
from typing import Any, Literal

from mcp.server import MCPServer
from herramientas import listar_articulos as obtener_publicados
from herramientas import crear_borrador as guardar_borrador


class BlogMCPServer(MCPServer):
    def run(
        self,
        transport: Literal["stdio", "sse", "streamable-http"] = "stdio",
        **kwargs: Any,
    ) -> None:
        if transport == "streamable-http":
            kwargs.setdefault("host", "127.0.0.1")
            kwargs.setdefault("port", 8001)
        try:
            super().run(transport=transport, **kwargs)
        except KeyboardInterrupt:
            pass


mcp = BlogMCPServer("Blog de robótica")

@mcp.tool()
def listar_articulos() -> list[dict]:
    """Lista los articulos publicados del blog de robótica."""
    return obtener_publicados()

@mcp.tool()
def crear_borrador(titulo: str, cuerpo: str) -> dict:
    """Crea un borrador NO publicado desde datos proporcionados."""
    return guardar_borrador(titulo, cuerpo)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")