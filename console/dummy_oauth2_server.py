import json
from string import Template
from typing import Optional
from urllib import request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, urlencode

HOST_NAME = "localhost"
PORT_NUMBER = 8000

main_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Oauth2</title>
</head>
<body>
<style>
    label, label > span {
        display: block;
    }

    label {
        margin: 15px 0;
    }
</style>

<a href="/">Home</a>

<form action="/get_url" method="post">
    <label>
        <span>Client ID</span>
        <input type="text" name="client_id" size=30 required>
    </label>
    <label>
        <span>Client Secret</span>
        <input type="text" name="client_secret" size=30 required>
    </label>
    <label>
        <span>Client URI</span>
        <input type="url" name="authorization_url" value="http://coub.com/oauth/authorize" size=30 required>
    </label>
    <label>
        <span>Redirect URI</span>
        <input type="url" name="callback_url" value="http://localhost:8000/callback" size=30 required>
    </label>
    <label>
        <span>Allowed Scopes</span>
        <textarea name="scope" cols="30" rows="7" required>
logged_in
create like
recoub
follow
channel_edit
        </textarea>
    </label>
    <label>
        <span>Allowed Response Types</span>
        <textarea name="response_type" cols="30" rows="1" required>code</textarea>
    </label>
    <button>Submit</button>
</form>
</body>
</html>
"""

token_html = Template(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>access_code</title>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <style type="text/css">
            div {
                display: block;
            }

            .main {
                background: #FFFFFF;
                box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.23);
                border-radius: 3px;
                width: 800px;
                text-align: center;
                margin: 0 auto;
            }

            .header {
                background: #5490E2;
                border-radius: 3px 3px 0px 0px;
                font-size: 19px;
                color: #FFFFFF;
                text-align: center;
                line-height: 30px;
                font-weight: bold;
            }

            .servicecontainer {
                margin-left: 40px;
                margin-top: 10px;
            }

            .key {
                font-size: 16px;
                text-align: left;
                padding-bottom: 5px;
                padding-top: 10px;
                font-weight: bold;
            }

            .value {
                text-align: left;
                color: #484848;
                margin-left: 70px;

            }

            .tokenval {
                padding: 12px;
                font-size: 20px;
                color: #000000;
                text-align: center;
                line-height: 28px;
                background: #F8FBFF;
                border: 2px dashed #A3CAFF;
                width: 80%;
                margin-left: 40px;
            }

            #tokenholder {
                text-align: center;
                display: inline-block;
                margin: 40px auto;
                width: 100%;
            }
        </style>
    </head>
<body>
<a href="/">Home</a>
<div class="main">

    <div class="header">
        <span style="font-weight: normal;">granted access from coub.com </span>
    </div>
    <div class="servicecontainer">
        <div class="key">requested scopes:</div>
        <div class="value">$scope</div>
        <div class="key">expired at:</div>
        <div class="value">$expired_at</div>
    </div>

    <div id="tokenholder">
        <div style="text-align: left;margin-left: 40px;margin-bottom: 10px;color: #232323;">Access Token</div>
        <div class="tokenval">$token</div>
    </div>
</div>
</body>
</html>

"""
)


def build_url(fields) -> str:
    url = fields[b"authorization_url"][0].decode("utf-8")

    params = {
        "redirect_uri": fields[b"callback_url"][0],
        "client_id": fields[b"client_id"][0],
        "response_type": fields[b"response_type"][0],
        "scope": " ".join(
            raw.decode("utf-8") for raw in (fields[b"scope"][0].split(b"\r\n")) if raw
        ),
    }
    return f"{url}?{urlencode(params)}"


def get_token(client_id: str, client_secret: str, redirect_url: str, code: str) -> dict:
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_url,
        "grant_type": "authorization_code",
    }
    data = urlencode(params).encode()
    req = request.Request("http://coub.com/oauth/token", data=data)
    response = request.urlopen(req)
    return json.loads(response.read())


def to_bytes(value: str) -> bytes:
    return bytes(value, "UTF-8")


class Oauth2Credentials:
    def __init__(self):
        self.client_id: Optional[str] = None
        self.client_secret: Optional[str] = None
        self.redirect_uri: Optional[str] = None

    def fill_credentials(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def is_ok(self) -> bool:
        return bool(self.redirect_uri and self.client_id and self.client_secret)


credentials = Oauth2Credentials()


class Oauth2Handler(BaseHTTPRequestHandler):
    def not_found(self):
        self._set_headers(status_code=404)

    def server_error(self):
        self._set_headers(status_code=500)
        self.wfile.write(to_bytes("<h1>Internal Server Error</h1>"))

    def get_url(self, fields):
        self._save_clients_params(fields)
        url = build_url(fields)
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

    def main(self):
        self._set_headers()
        content = to_bytes(main_html)
        self.wfile.write(content)

    def callback(self):
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get("code", [None])[0]
        if code is None or not credentials.is_ok():
            return self.server_error()

        response = get_token(
            credentials.client_id,
            credentials.client_secret,
            credentials.redirect_uri,
            code,
        )
        if "error" in response:
            self.server_error()
            self.wfile.write(to_bytes(response["error"]))
            return

        self._set_headers()
        expired_at = datetime.fromtimestamp(
            response["created_at"] + response["expires_in"]
        )
        content = token_html.substitute(
            **{
                "expired_at": expired_at,
                "token": response["access_token"],
                "scope": response["scope"],
            }
        )
        self.wfile.write(to_bytes(content))

    def _set_headers(self, status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _read_data(self):
        content_length = int(self.headers["Content-Length"])
        field_data = self.rfile.read(content_length)
        fields = parse_qs(field_data)
        return fields

    @staticmethod
    def _save_clients_params(fields):
        client_id = fields[b"client_id"][0].decode("utf-8")
        client_secret = fields[b"client_secret"][0].decode("utf-8")
        redirect_uri = fields[b"callback_url"][0].decode("utf-8")
        credentials.fill_credentials(client_id, client_secret, redirect_uri)

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        paths = {"/callback": self.callback, "/": self.main}

        path = urlparse(self.path).path
        if path in paths:
            paths[path]()
        else:
            self.not_found()

    def do_POST(self):
        paths = {"/get_url": self.get_url}
        fields = self._read_data()
        path = urlparse(self.path).path
        if path in paths:
            paths[path](fields)
        else:
            self.not_found()


def run(server_class=HTTPServer, handler_class=Oauth2Handler, port=PORT_NUMBER):
    server_address = (HOST_NAME, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd on http://{HOST_NAME}:{port}/ ...")
    httpd.serve_forever()


def main():
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
