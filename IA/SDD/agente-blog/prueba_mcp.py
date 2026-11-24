import asyncio
import json

from mcp import Client


async def main():
    async with Client("http://127.0.0.1:8001/mcp") as cliente:
        herramientas = await cliente.list_tools()
        print("Herramientas disponibles:")
        for herramienta in herramientas.tools:
            print("-", herramienta.name)

        resultado = await cliente.call_tool("listar_articulos", {})
        if resultado.is_error:
            raise RuntimeError(f"listar_articulos falló: {resultado.content}")

        articulos = resultado.structured_content
        if isinstance(articulos, dict) and "result" in articulos:
            articulos = articulos["result"]
        if articulos is None:
            articulos = [
                bloque.text
                for bloque in resultado.content
                if bloque.type == "text"
            ]
        print("\nArtículos publicados:")
        print(json.dumps(articulos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())