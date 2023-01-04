from urllib import request
from flask_admin import Admin
from flask_admin.contrib import sqla as flask_admin_sqla
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.menu import MenuLink
from flask_login import current_user
from flask import redirect, url_for, request



class DefaultModelView(flask_admin_sqla.ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwagrs):
        return redirect(url_for("auth.login", next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))

    @expose("/")
    def index(self):
        if not current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for("auth.login"))
        return super(MyAdminIndexView, self).index()