from os import path
import logging
import pprint
import re
import logging.config
from datetime import datetime
import yaml
from flask import Flask, json, request
from schema import Schema, Regex, And, Use

# date example: 
RE_DATE = r'^(?:(?:0[1-9])|(?:[1,2][0-9])|(?:3[0-1]))-(?:(?:0[1-9])|(?:1[0-2]))-\d{4}$'

# configure logging
log_conf = path.join(path.dirname(
    path.abspath(__file__)), 'logging.yaml')
with open(log_conf) as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))

app = Flask(__name__)


EVENT_SCHEMA = Schema({
    'jobid': Regex(r'^[-a-z0-9]+$'),
    'id_provider': int,
    'id_channel': int,
    'week': And(Regex(RE_DATE), Use(lambda x: datetime.strptime(x, '%d-%m-%Y'))),
    'href': Regex(r'^http(s)?://.+$', flags=re.I),
    'spider_name': And(str, len)})

@app.route('/service/hook', methods=['POST'])
def handle_event():
    try:
        event = EVENT_SCHEMA.validate(request.get_json())
        app.logger.info(pprint.pformat(event)) 
    except Exception as ex:
        app.logger.error(str(ex))
        return json.dumps({'failure': str(ex)}), 400
    else:    
        return json.dumps({'success': True}), 201


if __name__ == '__main__':
    app.run(debug=True)
