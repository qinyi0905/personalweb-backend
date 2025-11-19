from flask import Blueprint, render_template,request,current_app
from models.operation import LinkModel
from flask_paginate import get_page_parameter, Pagination

link_bp = Blueprint('link', __name__, url_prefix='/link')

@link_bp.route('/')
def link():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 6
    end = start + 6

    link_query = LinkModel.query.order_by(LinkModel.create_time.desc())

    total = link_query.count()
    links = link_query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, per_page=6, total=total,prev_label='上一页',next_label='下一页')

    context = {
        'links': links,
        'pagination': pagination,
    }
    return render_template('front/link.html', **context)

