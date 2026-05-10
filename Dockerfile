FROM python:3.10-slim

WORKDIR /code

# Cài đặt curl để kiểm tra health check nếu cần
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cấp quyền thực thi cho file chạy
RUN chmod +x start.sh

# HF Spaces yêu cầu chạy với user 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Chạy script khởi động
CMD ["./start.sh"]