import uvicorn

from FakeNewsDetection import app, config, uvicorn_log_config


if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT,  log_config=uvicorn_log_config)
