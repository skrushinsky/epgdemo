import logging
import re
import logging.config
from datetime import datetime
from flask import Flask, request
from schema import Schema, Regex, And, Use

# regexp for validating dates like: 19-04-2022
RE_DATE = r'^(?:(?:0[1-9])|(?:[1,2][0-9])|(?:3[0-1]))-(?:(?:0[1-9])|(?:1[0-2]))-\d{4}$'

# configure logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('journal')

app = Flask(__name__)


EVENT_SCHEMA = Schema({
    'jobid': Regex(r'^[-a-z0-9]+$'),
    'id_provider': int,
    'id_channel': int,
    'week': And(Regex(RE_DATE), Use(lambda x: datetime.strptime(x, '%d-%m-%Y'))),
    'href': Regex(r'^http(s)?://.+$', flags=re.I),
    'spider_name': And(str, len)})


@app.route('/')
def handle_root():
    return {'GET /': 'Index page', 'POST /service/hook': 'Post new event' }, 200



@app.route('/service/hook', methods=['POST'])
def handle_event():
    try:
        event = EVENT_SCHEMA.validate(request.get_json())
        logger.info({'message': 'success', 'event': event})
    except Exception as ex:
        logger.error({'message': 'failure', 'error': str(ex)})
        return {'failure': str(ex)}, 400
    else:    
        return {'success': True}, 201


@app.errorhandler(404)
def page_not_found(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description
    }, 404


def create_app():
    return Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
