from fastapi import FastAPI
import click

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@click.command()
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=8000, help="Port to run the server on")
def main(host: str, port: int):
    import uvicorn

    uvicorn.run(app, host=host, port=port)  # type: ignore


if __name__ == "__main__":
    main()
