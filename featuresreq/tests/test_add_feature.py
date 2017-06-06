
import unittest
import datetime
import json
from flask_sqlalchemy_session import current_session as session

from featuresreq.app import app
from featuresreq.models import FeatureRequest


class AddFeatureTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        # trigger database initialization on the first request
        self.app.get('/api/clients')

    def get_json(self, response):
        return json.loads(response.data.decode('utf8'))

    def test_get_clients(self):
        rv = self.app.get('/api/clients')
        data = self.get_json(rv)
        
        assert isinstance(data, list)
        assert len(data) == 3

        assert ["client a", "client b", "client c"] == [d['name'].lower() for d in data]
        assert all(d['id'] for d in data)

    def test_add_feature(self):
        with app.app_context():
            assert session.query(FeatureRequest).count() == 0

        data = dict(
            title="Test",
            description="Test D",
            client_id=2,
            priority=1,
            target_date='2017-05-03',
            product_area='Policies',
        )
        rv = self.app.post('/api/features', data=json.dumps(data))
        assert self.get_json(rv)['success'] == True

        with app.app_context():
            assert session.query(FeatureRequest).count() == 1
            fr = session.query(FeatureRequest).first()
            assert fr.title == data['title']
            assert fr.target_date.strftime("%Y-%m-%d") == data['target_date']

    def test_add_feature_invalid_client(self):
        data = dict(
            title="Test",
            description="Test D",
            client_id=10,
            priority=1,
            target_date='2017-05-03',
            product_area='Policies',
        )
        rv = self.app.post('/api/features', data=json.dumps(data))
        assert self.get_json(rv)['success'] == False

    def test_add_feature_invalid_feature(self):
        data = dict(
            title="Test",
            # missing description should fail
            client_id=1,
            priority=1,
            target_date='2017-05-03',
            product_area='Policies',
        )
        rv = self.app.post('/api/features', data=json.dumps(data))
        assert self.get_json(rv)['success'] == False
