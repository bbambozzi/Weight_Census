from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pytest
from app import Data

db = SQLAlchemy()  # We want to activate SQLAlchemy to mock the db and make comprehensive tests.


@pytest.fixture  # We use fixtures to make sure we're scalable.
def mock_orm_model():
    My_Model = Data("test@test.com", 70)  # Grab the app's data structure
    My_Model.id = "test_id"  # We manually change the ID to something we can recognize later.
    return My_Model


@pytest.fixture
def mock_db_object():
    class MockObject(Data):  # We'll create a mock object to make sure everything is working correctly.
        local_weight = 1337
        local_email = "some_address"

        def transform_to_json(self):  # We transform it into a JSON for easy access.
            return {
                "some_value": self.local_weight,
                "some_address": self.local_email
            }
    return MockObject


def test_mock_db_object(mock_db_object):
    mock_db_object.local_email = "test@testerino.com"  # We modify the values to make sure it's transformed correctly.
    mock_db_object.local_weight = 1
    assert mock_db_object.transform_to_json(mock_db_object)["some_value"] == 1  # We check with a new value
    assert mock_db_object.transform_to_json(mock_db_object)["some_address"] == "test@testerino.com"  # We check again.


def test_SQLAlchemy_db_mock(mock_orm_model):  # We're checking the mocked db model to test if it works out correctly.
    my_model = mock_orm_model
    assert my_model.id == "test_id"
    assert my_model.local_weight == 70
    assert my_model.local_email == "test@test.com"
