# WutheringWaves Login Service

一个用于 WutheringWavesUID 的外置登录服务。

## 功能特性

- 库街区手机验证码登录

## 环境要求

- Python 3.10+
- Docker (可选，用于容器化部署)

## 本地开发

### 使用 uv (推荐)

1. 安装依赖：
```bash
uv sync
```

2. 启动服务：
```bash
uv run start
```

### 使用 pip

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动服务：
```bash
python start.py
```

## Docker 部署

1. 构建镜像：
```bash
docker build -t ww-login .
```

2. 运行容器：
```bash
docker run -d -p 7860:7860 ww-login
```

## 配置说明

服务配置可以通过环境变量或 `.env` 文件设置：

- `HOST`: 服务监听地址（默认：127.0.0.1）
- `PORT`: 服务端口（默认：7860）

## 部署建议

1. 生产环境建议使用 Docker 部署
2. 建议配置反向代理（如 Nginx）
3. 建议启用 HTTPS
4. 注意配置适当的访问控制

## 许可证

MIT License