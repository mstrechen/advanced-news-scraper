from flask_security import RegisterForm as BaseRegisterForm
from flask_security.forms import Required
from wtforms import StringField


class RegisterForm(BaseRegisterForm):
    full_name = StringField('Full name', [Required()])
