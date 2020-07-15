import os 
import pytest
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock
from flask.testing import FlaskClient
from flask import url_for, Response, current_app, redirect, render_template, Flask
from models.quickbooks_position import QuickbooksPosition
from quickbooks.views import SavePosition

def test_save_quickbook_position_200(client: FlaskClient, app):
    position = SavePosition()
    data = {
        "submitter" : "dummy",
        "as_of_date": datetime.utcnow(),
        "period" : "2020-07-11",
        "wisetack_junior_position" : 12.12,
        "lighter_junior_position" : 15
    }  
    with app.app_context():
        url = url_for('quickbooks.save_position')
    response = client.post(url,data=data)
    assert response.status_code == 200
    assert "testing.domain/save_position" in url

def test_no_wisetack_junior_(client: FlaskClient, app):
    data = {
        "submitter" : "dummy",
        "as_of_date": datetime.utcnow(),
        "period" : "2020-07-11",
        "lighter_junior_position" : 15
    }  
    with app.app_context():
        url = url_for('quickbooks.save_position')
    with pytest.raises(ValueError, match="Please enter a value for Wisetack Junior position"):    
        response = client.post(url,data=data)
        assert response.status_code == 200

def test_no_lighter_junior_position(client: FlaskClient, app):
    data = {
        "submitter" : "dummy",
        "as_of_date": datetime.utcnow(),
        "period" : "2020-07-11",
        "wisetack_junior_position" : 154.5
    }  
    with app.app_context():
        url = url_for('quickbooks.save_position')
    with pytest.raises(ValueError, match="Please enter a value for Lighter Junior position"):    
        response = client.post(url,data=data)
        assert response.status_code == 200


def test_request_task_status_200(client: FlaskClient, app):
    with app.app_context():
        url = url_for('quickbooks.form_quickbook')
    response = client.get(url)
    assert response.status_code == 200


def test_mock_save_position_200(mocker: MagicMock, client: FlaskClient, app):
    decode_token = mocker.patch("quickbooks.views.SavePosition.post", return_value={})
    with app.app_context():
        url = url_for('quickbooks.save_position', form={})
    response = client.post(url)
    assert response.status_code == 200
    decode_token.assert_called_once()
