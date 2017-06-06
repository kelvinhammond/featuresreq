
import os
from featuresreq.factory import create_app

DB_URI = os.environ.get('FEATURES_REQ_DB_URI', 'sqlite://')
app = create_app(db_uri=DB_URI)

