# Copyright: 2013 Bastian Blank <bastian@waldi.eu.org>
# License: BSD 2-clause, see LICENSE for details.

import os
import time

from flask import Flask, render_template

from .storage import create_storage
from .views import blueprint
from .utils.name import setup_werkzeug_routing
from .utils.permissions import *


def create_app():
    app = Flask(__name__)

    app.config.from_object('bepasty.config.Config')
    if os.environ.get('BEPASTY_CONFIG'):
        app.config.from_envvar('BEPASTY_CONFIG')

    create_storage(app)
    setup_werkzeug_routing(app)

    app.register_blueprint(blueprint)

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('_error_403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('_error_404.html'), 404

    def datetime_format(ts):
        """
        takes a unix timestamp and outputs a iso8601-like formatted string.
        times are always UTC, but we don't include the TZ here for brevity.
        it should be made clear (e.g. in the template) that the date/time is UTC.
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))

    app.jinja_env.filters['datetime'] = datetime_format

    app.jinja_env.globals['logged_in'] = logged_in
    app.jinja_env.globals['get_permissions'] = get_permissions
    app.jinja_env.globals['may'] = may
    app.jinja_env.globals['PERMISSIONS'] = PERMISSIONS
    app.jinja_env.globals['ADMIN'] = ADMIN
    app.jinja_env.globals['CREATE'] = CREATE
    app.jinja_env.globals['READ'] = READ
    app.jinja_env.globals['DELETE'] = DELETE

    return app
