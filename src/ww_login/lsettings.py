from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 7860

    class Config:
        env_file = ".env"  # 指定 .env 文件的路径
        env_file_encoding = "utf-8"


lsettings = Settings()
