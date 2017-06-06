
from marshmallow_sqlalchemy import ModelSchema

from featuresreq.models import Client, FeatureRequest


class ClientSchema(ModelSchema):
    class Meta:
        model = Client
        fields = ('id', 'name')


class FeatureRequestSchema(ModelSchema):
    class Meta:
        model = FeatureRequest
        load_only = ('id',)
        fields = ('title', 'description', 'client_id', 'priority', 
                  'target_date', 'product_area')

