import json
import requests
import datetime
from flask import Flask,render_template, redirect, url_for, request, current_app, Blueprint
from datetime import datetime
from flask.views import MethodView
from jinja2 import Markup
from flask_sqlalchemy import SQLAlchemy
from models.quickbooks_position import QuickbooksPosition
from services.db import DB as db
from hcg_utils.authentication.utils import current_user

QUIKBOOKS = Blueprint('quickbooks',__name__, template_folder='templates')

class FormQuickbook(MethodView):
    def get(self):
        return render_template(
            'quickbooks/quickbook-position.html'
        )

class SavePosition(MethodView):
    def post(self):
        req = request.form
        period = req.get('period')
        print(period)
        as_of_date = datetime.now()
        submitter = current_user.identifier
        if req.get('wisetack_junior_position') == '':
            wisetack_junior_position = 0.00   
        else:
            wisetack_junior_position = req.get('wisetack_junior_position')
        if req.get('lighter_junior_position') == '':
            lighter_junior_position = 0.00
        else:
            lighter_junior_position = req.get('lighter_junior_position') 
        position = QuickbooksPosition(submitter,as_of_date,period,wisetack_junior_position,lighter_junior_position)
        try:
            db.create_all()
            db.session.add(position)
            db.session.commit()
        except Exception:
            current_app.logger.exception('Please verify your data')
            return render_template(
                'quickbooks/error-page.html'
            )
        return render_template(
            'quickbooks/success-page.html'
        )


QUIKBOOKS.add_url_rule('/', view_func=FormQuickbook.as_view('form_quickbook'))
QUIKBOOKS.add_url_rule('/save_position', view_func=SavePosition.as_view('save_position'))