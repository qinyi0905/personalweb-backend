from flask import Blueprint, render_template,request,redirect
from models.operation import ToolModel,ToolTypeModel
from flask_paginate import get_page_parameter, Pagination
from exts import db
from utils import restful

tool_bp = Blueprint('tool', __name__, url_prefix='/tool')

@tool_bp.route('/')
def tool():
    type_id = request.args.get("type", type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    start = (page - 1) * 6
    end = start + 6

    tool_query = ToolModel.query.order_by(ToolModel.create_time)

    if type_id:
        tool_query = tool_query.filter(ToolModel.type_id==type_id)
    total = tool_query.count()
    tools = tool_query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, per_page=6, total=total,prev_label='上一页',next_label='下一页',show_single_page=True)

    tool_types = ToolTypeModel.query.order_by(ToolTypeModel.priority.desc()).all()
    context = {
        'tool_types': tool_types,
        'tools': tools,
        'pagination': pagination,
        'type_id': type_id,
    }
    return render_template('front/tool.html',**context)


@tool_bp.route('/use/<int:tool_id>')
def use_tool(tool_id):
    # 查询工具
    tool = ToolModel.query.get(tool_id)
    if not tool:
        return restful.params_error(message="参数错误")
    # 增加访问次数
    tool.access_count += 1
    db.session.commit()
    # 重定向到实际工具链接
    return  redirect(tool.link_url)