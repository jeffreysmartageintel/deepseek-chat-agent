# 使用Python 3.11作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/

# 暴露端口（Google Cloud Run默认使用8080）
EXPOSE 8080

# 设置启动命令 - 使用启动脚本，确保正确监听端口
# 启动脚本会先启动健康检查服务器，然后启动 Gradio 应用
# 使用 JSON 数组格式（exec 格式）以确保信号正确处理
CMD ["python", "-m", "app.start_server"]

