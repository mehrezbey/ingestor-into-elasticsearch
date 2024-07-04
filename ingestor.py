from elasticsearch import Elasticsearch  # type: ignore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from elasticsearch.helpers import bulk, BulkIndexError # type: ignore
import os


data_base_name = "nation"
URI = "mysql+pymysql://root:@localhost:3307/"
username=os.environ.get('ELASTIC_USERNAME')
password = os.environ.get('ELASTIC_PASSWORD')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI + data_base_name
db = SQLAlchemy(app)

client = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=(username, password),
    request_timeout = 60
    )
database_schema = []
if client.ping():
    print("Connected to Elasticsearch!")
else:
    print("Could not connect to Elasticsearch!")
    exit()
def ingest_data_to_elasticsearch(batch_size=500):
    Base = automap_base()
    with app.app_context():
        Base.prepare(db.engine,reflect=True)
        tables = Base.classes.keys()
        for table_name in tables:
            table={}
            model = Base.classes[table_name]
            table["table_name"] = table_name
            rows = db.session.query(model).all()
            columns = model.__table__.columns.keys()
            table["columns"]= columns
            database_schema.append(table)
            total_rows = db.session.query(model).count()
            for start in range(0, total_rows, batch_size):
                rows = db.session.query(model).offset(start).limit(batch_size).all()
                data = [
                    {
                        '_index': data_base_name +"-"+table_name.lower(),
                        '_source': {col: getattr(row, col) for col in columns}
                    }
                    for row in rows
                ]
                try:
                    bulk(client, data)
                except BulkIndexError as e:
                    for error in e.errors:
                        print("Error indexing document:", error)
                    raise
        print("Data was successfully indexed into ElasticSearch")
        print(database_schema)
ingest_data_to_elasticsearch()