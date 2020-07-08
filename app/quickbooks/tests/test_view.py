import os 
import pytest
from unittest import mock
from unittest.mock import MagicMock
from flask.testing import FlaskClient
from flask import url_for, Response, current_app, redirect, render_template, Flask


def test_request_task_status_200(mocker: MagicMock, client: FlaskClient, app):
    decode_token = mocker.patch("quickbooks.views.FormQuickbook.get", return_value={})
    with app.app_context():
        url = url_for('quickbooks.form_quickbook')
    response = client.get(url)
    assert response.status_code == 200
    decode_token.assert_called_once()

def test_save_position_200(mocker: MagicMock, client: FlaskClient, app):
    decode_token = mocker.patch("quickbooks.views.SavePosition.post", return_value={})
    with app.app_context():
        url = url_for('quickbooks.save_position', form={})
    response = client.post(url)
    assert response.status_code == 200
    decode_token.assert_called_once()

def test_save_position_202(mocker: MagicMock, client: FlaskClient, app):
    decode_token = mocker.patch("quickbooks.views.SavePosition.post", return_value='SUCCESS')
    with app.app_context():
        url = url_for('quickbooks.save_position')
    response = client.post(url)
    db = current_app.extensions['sqlalchemy'].db
    assert response.status_code == 202
    decode_token.assert_called_once()
   