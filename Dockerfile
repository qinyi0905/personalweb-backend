FROM nginx:1.26.2

RUN mkdir -p /var/log/personalweb && mkdir -p /app && mkdir -p ~/.pip

WORKDIR /app

COPY apps /app/apps/
COPY media /app/media/
COPY models /app/models/
COPY templates /app/templates/
COPY static /app/static/
COPY utils /app/utils/
COPY *.py pip.conf requirements.txt nginx.conf start_server.sh /app/

RUN sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    cd /app && \
    apt install -y python3 python3-pip python3-venv procps iputils-ping ncat redis-tools vim && \
    python3 -m venv venv && \
    . ./venv/bin/activate && \
    cp /app/pip.conf ~/.pip/pip.conf && \
    ./venv/bin/pip3 install --no-cache-dir -r requirements.txt && \
    ./venv/bin/pip3 install sqlalchemy-serializer==1.4.22 --no-deps && \
    cat /app/nginx.conf > /etc/nginx/conf.d/default.conf  && \
    cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf /app/utils/captcha/ && \
    rm -rf /app/utils/captcha/verdana.ttf || true

ENV FLASK_APP=app.py
ENV PYTHONPATH=/app