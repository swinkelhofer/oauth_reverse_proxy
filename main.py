from oauth.oauth_flask import *
from flask import Response, request, Flask, redirect, render_template
import requests
import socket
import re
import urllib
import json
import os

VERSION = '1.0.0'
app = Flask(__name__, static_url_path='', 
            static_folder='something_Flask_really_ignores/static')
url_map = app.url_map
try:
    for rule in url_map.iter_rules('static'):
        url_map._rules.remove(rule)
except:
    pass
d = {}
d['oauth_client_id'] = os.getenv('OAUTH_CLIENT')
d['oauth_client_secret'] = os.getenv('OAUTH_SECRET')
d['client_uri'] = '%s://%s' % (os.getenv('PROTOCOL'), os.getenv('DOMAIN'))
oauth = OAuth(**d)
oauth.load_defaults(provider=os.getenv("OAUTH_PROVIDER", "gitlab"), provider_uri=os.getenv("OAUTH_PROVIDER_URI"))
oauth.default_routes(sign_in = os.getenv("OAUTH_SIGNIN_ROUTE", "/sign_in"), sign_out = os.getenv("OAUTH_SIGNOUT_ROUTE", "/logout"), get_token = os.getenv("OAUTH_REDIRECT_ROUTE", "/auth"), app = app)

def proxy(path):
    try:
        # print "http://etherpad:9001%s%s" % (path, data)
        # if request.method == "GET":
        #     r = requests.get("http://etherpad:9001%s%s" % (path, data), headers=request.headers)
        # elif request.method == "POST":
        #     try:
        #         r = requests.post("http://etherpad:9001%s%s" % (path, data), headers=request.headers, data=request.get_data())
        #     except:
        #         raise
        #         r = requests.post("http://etherpad:9001%s%s" % (path, data), headers=request.headers, data=request.form)
        #     # r = requests.post("http://etherpad:9001%s" % (path, data), headers=request.headers, data=request.form)
        headers = {key: value for (key, value) in request.headers if key != 'Host'}
        headers['X-Forwarded-Proto'] = os.getenv('PROTOCOL', 'http')
        headers['Host'] = os.getenv(os.getenv('DOMAIN'))
        request.environ['CONTENT_TYPE'] = 'application/something_Flask_ignores'
        r = requests.request(
            method=request.method,
            url=request.url.replace(os.getenv("DOMAIN"), "%s:%s" % (os.getenv("UPSTREAM_HOSTNAME"), os.getenv("UPSTREAM_PORT"))),
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            allow_redirects=True,
            cookies=request.cookies)
        excluded_headers = ['content-type', 'content-encoding', 'transfer-encoding', 'content-length']
        headers = [(name, value) for (name, value) in r.raw.headers.items()
               if name.lower() not in excluded_headers]

        try:
            mimetype = r.headers.get('content-type').split(';')[0] 
        except:
            mimetype = "text/html"
        return Response(r.content, headers = headers, status = r.status_code, mimetype=mimetype)
    except:
        return Response("Internal Server Error", status=500)

@app.route('/', methods=['GET', 'POST'])
def home():
    if oauth.is_oauth_session() == False:
        return make_response(render_template('signin.html'))
    elif oauth.is_oauth_session() == True:
        return proxy("/") 

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
@oauth.protect(role='all')
def catch_all(path):
    return proxy(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
