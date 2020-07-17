import json
import requests
import datetime
from flask import (
    Flask, render_template, redirect, url_for,
    request, current_app, Blueprint, Response
)
from datetime import datetime
from flask.views import MethodView
from jinja2 import Markup
from flask_sqlalchemy import SQLAlchemy
from models.quickbooks_position import QuickbooksPosition
from services.db import DB as db
from hcg_utils.authentication.utils import current_user

from .forms import QuickBooksForm


QUICKBOOKS = Blueprint('quickbooks',__name__, template_folder='templates')

class FormQuickbook(MethodView):
    def get(self):
        form = QuickBooksForm(request.form)
        return render_template(
            'quickbooks/quickbook-position.html',
            form=form
        )

    def post(self):
        form = QuickBooksForm(request.form)

        if not form.validate():
            return render_template(
                'quickbooks/quickbook-position.html',
                form=form
            ), 400

        if current_user.authenticated is False:
            return render_template(
                'quickbooks/error-page.html',
                exception='Could not determine current user, not saving',
            ) , 400

        position = QuickbooksPosition(
            submitter=current_user.identifier,
            as_of_date=datetime.utcnow(),
            period=form.period.data,
            wisetack_junior_position=form.wisetack_junior_position.data,
            lighter_junior_position=form.lighter_junior_position.data
        )
        try:
            db.session.add(position)
            db.session.commit()
        except Exception as ex:
            current_app.logger.exception('could not persist entry')
            return render_template(
                'quickbooks/error-page.html',
                exception=str(ex),
            ) , 400

        return render_template(
            'quickbooks/success-page.html'
        )

QUICKBOOKS.add_url_rule('/', view_func=FormQuickbook.as_view('data_entry'))
