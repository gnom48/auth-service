if __name__ == "__main__":
    import uvicorn

    from .rest.server import asgi_application
    from .configs import ServerConfig

    server_config = ServerConfig()

    uvicorn.run(
        asgi_application,
        host="0.0.0.0",
        port=server_config.SERVER_PORT,
        root_path=server_config.ROOT_PATH
    )
