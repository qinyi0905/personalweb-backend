FROM nginx:1.26.2

RUN mkdir -p /var/log/personalweb && mkdir -p /app

WORKDIR /app

COPY * /app/

RUN cd /app && \
    apt install -y python3 python3-pip python3-venv && \
    python3 -m venv venv && \
    . venv/bin/activate \
    ./venv/bin/pip3 install --no-cache-dir -r requirements.txt && \
    ./venv/bin/pip3 install sqlalchemy-serializer==1.4.22 --no-deps && \
    cat /app/entrypoint.sh > /docker-entrypoint.sh

ENV FLASK_APP=/app/app.py