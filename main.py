from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from flask import Flask, request, Response
from flask_pymongo import PyMongo
import json
import os
from pymongo.errors import ConnectionFailure, AutoReconnect, ServerSelectionTimeoutError
from modules.label_image import Filter
from modules.file_url import Files
from stores.image_filter_store import ImageFilterStore


MONGO_URL = "127.0.0.1:27017/troph"
client = None
store = ImageFilterStore()
app = Flask(__name__)


def label_img(img_id, img_source, img_url):
    global client
    nsfw_filter = Filter(image_id=img_id,
                         image_source=img_source, image_url=img_url)
    try:
        results = nsfw_filter.label_image()
        if client is None:
            app.config["MONGO_URI"] = "mongodb://{}".format(os.environ.get("MONGO"))
            client = PyMongo(app)
        store.insert(client.db, results)
    except (AutoReconnect, ServerSelectionTimeoutError) as error:
        raise RuntimeError('server not available: {}'.format(error))
    except Exception as e:
        raise e
    return results

def label_img_volc(img_url):
    global client
    nsfw_filter = Filter(image_id=None,
                         image_source=None, image_url=img_url)
    try:
        results = nsfw_filter.label_image_volc()
    except Exception as e:
        raise e
    return results


# -------------- Test Routes ----------------
@app.route('/', methods=['GET'])
def home():
    return '''<h1>TEST</h1>
<p>The connection works</p>'''


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/imagefilter', methods=['POST'])
def filter_image():
    # image_id = 'https://p3-imagex.byteimg.com/obj/tos-cn-i-c226mjqywu/524a08a7828843ac9a6c8cb37b9ce674'
    if request.method == 'POST':
        try:
            r = request.json
        except Exception:
            raise RuntimeError("Failed to get json")
        results = label_img_volc(r['img_url'])

    json_response = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    return response


# -------------- Image Filter Routes ----------------
@app.route('/imagefilter/avatars/<image_id>', methods=['GET'])
def get_avatar_filter(image_id):
    # local_test: http://127.0.0.1:5001/avatars/1f5a5f34b4a0b280438afd08fa78f70c/filter?format=png
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No avatar format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.avatar_url()

    if request.method == 'GET':
        results = label_img(image_id, 'avatar', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.route('/imagefilter/emojis/<image_id>', methods=['GET'])
def get_emoji_filter(image_id):
    # test: http://127.0.0.1:5001/emojis/77700447472717824/filter?format=png
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No emoji format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.emoji_url()

    if request.method == 'GET':
        results = label_img(image_id, 'emoji', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.route('/imagefilter/icons/<image_id>', methods=['GET'])
def get_icon_filter(image_id):
    # http://localhost:5001/imagefilter/icons/e8bf028396e06208a6401fb8a2e19d29?format=png
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No icon format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.icon_url()

    if request.method == 'GET':
        results = label_img(image_id, 'icon', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.route('/imagefilter/backgrounds/<image_id>', methods=['GET'])
def get_background_filter(image_id):
    # test: http://127.0.0.1:5001/backgrounds/16962aad80d5682141c05112a9fb90ce/filter?format=png
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No background format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.background_url()

    if request.method == 'GET':
        results = label_img(image_id, 'background', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.route('/imagefilter/attachments/<image_id>', methods=['GET'])
def get_attachment_filter(image_id):
    # test: http://127.0.0.1:5001/attachments/532b3b39c804a59d1e2e2462dbaf6606/filter?format=png
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No attachment format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.attachment_url()

    if request.method == 'GET':
        results = label_img(image_id, 'attachment', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.route('/imagefilter/stamps/<image_id>', methods=['GET'])
def get_stamp_filter(image_id):
    # test: http://127.0.0.1:5001/stamps/e49d90eb5465dce083a4628aaa248f92/filter?format=png
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No stamp format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.stamp_url()

    if request.method == 'GET':
        results = label_img(image_id, 'stamp', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.route('/imagefilter/externals/<image_id>', methods=['GET'])
def get_external_filter(image_id):
    # test: http://127.0.0.1:5001/externals/901473e25d35d57c7d76ce5fa418705b/filter?format=jpeg
    # http://127.0.0.1:5001/externals/a8b9ef2ed70faea3c6847ba8f0afb5a3/filter?format=gif
    if 'format' in request.args:
        img_format = request.args['format']
    else:
        return "Error: No external format field provided."

    image_file = Files(image_id + '.' + img_format)
    image = image_file.external_url()

    if request.method == 'GET':
        results = label_img(image_id, 'external', image)

    return json.dumps(results, indent=4, sort_keys=True)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":

    try:
        if os.environ.get("MONGO"):
            MONGO_URL = os.environ.get("MONGO")
        app.config["MONGO_URI"] = "mongodb://{}".format(MONGO_URL)
        client = PyMongo(app)
    except (ServerSelectionTimeoutError, ConnectionFailure, AutoReconnect):
        print('Server not available')
    except Exception as e:
        print(e)
        raise

    # app.run(host='0.0.0.0', port=5001, debug=True)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
