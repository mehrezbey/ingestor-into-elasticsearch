
# Ingestor Program

## Overview

The Ingestor program extracts data from a relational database (MariaDB in this example) and indexes it into Elasticsearch. It serves as a bridge between traditional relational databases and Elasticsearch for efficient data retrieval and analysis.

## Requirements

- Python 3.x installed on your system ([Download Python](https://www.python.org/downloads/))
- Elasticsearch installed and configured ([Install Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html))

## requirements.txt
flask
elasticsearch
pymysql

## Configuration
Before running the Ingestor program, make sure to configure the following parameters according to your environment:

- Database Settings:

    - Database Name: Replace "nation" with your actual database name.
    - Database URI: Replace mysql+pymysql://root:@localhost:3307/ with your database URI. Modify the username, password, host, and port as needed. You can use environment variables (os.environ.get) for sensitive information like passwords.

- Elasticsearch Settings:

    - Ensure Elasticsearch is running and accessible.
    - Optionally, edit the environment variables (ELASTIC_USERNAME and ELASTIC_PASSWORD) to securely provide credentials.

## Usage
1. Activate Virtual Environment:
```bash
source path_to_your_virtualenv/bin/activate  # Linux/Mac
path_to_your_virtualenv\Scripts\activate    # Windows
```

2. Install requirements 
```bash
pip install -r requirements.txt
```

3. Run the Ingestor Program:
```bash
python ingestor.py
```

This will start ingesting data from your database into Elasticsearch, allowing you to query your indices using Python or any programming language or through Kibana for enhanced performance and visualization.
