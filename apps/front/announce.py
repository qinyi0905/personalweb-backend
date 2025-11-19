from flask import Blueprint, render_template, request, current_app
from flask_paginate import get_page_parameter, Pagination
from models.operation import AnnounceModel
from exts import db  # 需要导入 db 来操作数据库

announce_bp = Blueprint('announce', __name__, url_prefix='/announce')

@announce_bp.route('/')
def announce():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 5
    end = start + 5

    announce_obj = AnnounceModel.query.filter_by(is_active=True).order_by(AnnounceModel.create_time.desc())

    # 获取当前选中的公告ID，默认为最新的一条公告
    select_id = request.args.get("si", announce_obj.first().id if announce_obj.first() else None, type=int)

    # 新增部分：如果存在select_id，则增加访问次数
    if select_id:
        selected_announce = AnnounceModel.query.get(select_id)
        if selected_announce:
            selected_announce.access_count += 1
            db.session.commit()

    announces = announce_obj.all()
    total = announce_obj.count()
    announce_slices = announce_obj.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, per_page=5, total=total)

    context = {
        'announce_slices': announce_slices,
        'announces': [announce.to_dict() for announce in announces],
        'pagination': pagination,
        'si': select_id,
        'page': page
    }

    return render_template('front/announce.html', **context)
