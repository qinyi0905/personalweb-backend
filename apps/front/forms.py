from wtforms import Form,ValidationError
from wtforms.fields import StringField, IntegerField
from wtforms.validators import InputRequired, Length
from exts import cache
from flask import request

class BaseForm(Form):
  @property
  def messages(self):
    message_list = []
    if self.errors:
      for errors in self.errors.values():
        message_list.extend(errors)
    return message_list


class LoginForm(BaseForm):
    username = StringField(validators=[InputRequired(message="请输入正确的用户名！")])
    password = StringField(validators=[Length(6, 20, message="请输入正确长度的密码！")])
    graph_captcha = StringField(validators=[Length(4, 4, message="请输入正确的图形验证码！")])

    def validate_graph_captcha(self, field):
        key = request.cookies.get("_graph_captcha_key")
        cache_captcha = cache.get(key)
        graph_captcha = field.data
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message="图形验证码错误！")