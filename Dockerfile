FROM python:3.13.2-slim-bookworm

WORKDIR /app

# 复制依赖配置到工作目录
COPY requirements.txt .

# 安裝依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目到/app
COPY src src

# 绑定宿主机时需要应用监听 0.0.0.0
ENV FLASK_RUN_HOST=0.0.0.0

# 入口设置为你的Flask启动文件
CMD ["python", "src/flask/flast_main.py"]