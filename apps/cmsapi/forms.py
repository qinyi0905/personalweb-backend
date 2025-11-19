from wtforms import Form
from wtforms.fields import FileField, StringField, IntegerField
from wtforms.validators import InputRequired,Length
from flask_wtf.file import FileAllowed, FileSize


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.extend(errors)
        return message_list


class UploadImageForm(BaseForm):
    image_url = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="图片格式不符合要求！"),
                                  FileSize(max_size=1024 * 1024 * 10, message="图片最大不能超过10M！")])
    icon_url = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="图片格式不符合要求！"),
                                      FileSize(max_size=1024 * 1024 * 10, message="图片最大不能超过10M！")])


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])


class AddAnnounceForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入标题！"), Length(min=1, max=100, message="标题长度在1-100之间！")])
    content = StringField(validators=[InputRequired(message="请输入内容！")])

class AddToolTypeForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入名称！"), Length(min=1, max=30, message="名称长度在1-30之间！")])
    priority = IntegerField(validators=[InputRequired(message="请输入优先级！")])
    icon = StringField(validators=[InputRequired(message="请选择图标！")])

class AddToolForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入名称！"), Length(min=1, max=30, message="名称长度在1-30之间！")])
    description = StringField(validators=[InputRequired(message="请输入描述！")])
    icon_url = StringField(validators=[InputRequired(message="请输入图标链接！")])
    link_url = StringField(validators=[InputRequired(message="请输入链接！")])
    type_name = StringField(validators=[InputRequired(message="请选择分类！")])

class AddLinkForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入名称！"), Length(min=1, max=30, message="名称长度在1-30之间！")])
    link_url = StringField(validators=[InputRequired(message="请输入链接！")])

class AddUserForm(BaseForm):
    username = StringField(validators=[InputRequired(message="请输入用户名！"), Length(min=1, max=30, message="用户名长度在1-30之间！")])
    password = StringField(validators=[InputRequired(message="请输入密码！"), Length(min=6, max=30, message="密码长度在6-30之间！")])
    realname = StringField(validators=[InputRequired(message="请输入真实姓名！"), Length(min=1, max=30, message="真实姓名长度在1-30之间！")])
    role_id = IntegerField(validators=[InputRequired(message="请选择角色！")])