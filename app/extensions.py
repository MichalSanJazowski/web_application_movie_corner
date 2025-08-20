from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_session import Session

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()
ckeditor = CKEditor()
session_ext = Session()
