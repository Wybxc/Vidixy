from pathlib import Path
import click


@click.command()
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=8000, help="Port to run the server on")
@click.option(
    "--nodes",
    default="nodes",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to the nodes directory",
)
@click.option("--reload", is_flag=True, help="Reload the server on code changes")
def main(host: str, port: int, nodes: str, reload: bool):
    import uvicorn
    from .application import app
    from .nodes import load_nodes

    load_nodes(Path(nodes))

    from .nodes import VidixyNode

    print(VidixyNode.sockets)
    print(VidixyNode.nodes)

    uvicorn.run(app, host=host, port=port, reload=reload)  # type: ignore


if __name__ == "__main__":
    main()
