FROM nginx:1.26.2

RUN mkdir -p /var/log/personalweb && mkdir -p /app && mkdir -p ~/.pip

WORKDIR /app

RUN cp -r apps /app/ && \
    cp -r media /app/ && \
    cp -r models /app/ && \
    cp -r templates /app/ && \
    cp -r static /app/ && \
    cp -r utils /app/ && \
    cp entrypoint.sh /app/ && \
    cp *.py /app/ && \
    cp pip.conf /app/ && \
    cp requirements.txt /app/ \
    cp nginx.conf /app/

RUN sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    cd /app && \
    apt install -y python3 python3-pip python3-venv && \
    python3 -m venv venv && \
    source ./venv/bin/activate && \
    cp /app/pip.conf ~/.pip/pip.conf && \
    ./venv/bin/pip3 install --no-cache-dir -r requirements.txt && \
    ./venv/bin/pip3 install sqlalchemy-serializer==1.4.22 --no-deps && \
    cat /app/entrypoint.sh > /docker-entrypoint.sh

ENV FLASK_APP=app.py