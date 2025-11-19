from flask import Blueprint, send_from_directory, current_app

media_bp = Blueprint("media", __name__, url_prefix="/media")

@media_bp.route("/banner/<filename>")
def get_banner_image(filename):
    return send_from_directory(current_app.config['BANNER_IMAGE_SAVE_PATH'], filename)


@media_bp.route("/tool/icon/<filename>")
def get_tool_icon_image(filename):
    return send_from_directory(current_app.config['TOOL_ICON_SAVE_PATH'], filename)