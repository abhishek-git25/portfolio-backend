from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="Portfolio Backend")
    return app
