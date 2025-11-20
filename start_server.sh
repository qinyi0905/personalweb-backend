#!/bin/bash

source /app/venv/bin/activate

rm -rf /app/migrations || true

# 初始化数据库（如果尚未初始化）
flask db init || true

# 生成迁移脚本
flask db migrate

# 应用数据库迁移
flask db upgrade

#加入初始数据
flask init_roles
flask init_admin_user

# gunicorn启动 Flask 应用
gunicorn app:app