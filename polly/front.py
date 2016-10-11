from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

import helpers
import core
import errors

class Handler:
    def __call__(self, method, route_args, data):
        if method == 'GET':
            return self.get(route_args)
        elif method == 'POST':
            return self.post(route_args, data)


class PageHandler(Handler):
    pass


class EventHandler(Handler):
    def get(self, route_args):
        event = core.Event.get_latest(route_args['event_id'])
        return helpers.json_encode(event)

    def post(self, route_args, data):
        pass


class AccreditationHandler(Handler):
    def get(self, route_args):
        pass

    def post(self, route_args, data):
        pass


class QuestionHandler(Handler):
    def get(self, route_args):
        pass

    def post(self, route_args, data):
        pass


def match(url, method):

    routes = [
        ('', PageHandler),
        ('event', EventHandler),
        ('event/:event_id', EventHandler),
        ('event/:event_id/question/:question_id', QuestionHandler),
        ('event/:event_id/question/:question_id/:opening_type', QuestionHandler),
        ('event/:event_id/question/:question_id/vote/:member_id', QuestionHandler),
        ('event/:event_id/accreditation/:member_id', AccreditationHandler)
    ]

    url_parts = url.split('/')

    for route in routes:
        route_parts = route[0].split('/')

        if len(route_parts) != len(url_parts):
            continue

        route_args = {}
        for i in range(len(route_parts)):
            if route_parts[i][0] == ':':
                route_args[route_parts[i][1:]] = url_parts[i]
                continue
            elif route_parts[i] == url_parts[i]:
                continue
            else:
                break
        else:
            break
    else:
        print('NO MATCH')
        exit()

    return (route[1](), route_args)


def front(environ, start_response):
    setup_testing_defaults(environ)

    url = environ['PATH_INFO']
    url_parts = url.strip('/').split('/')
    method = environ['REQUEST_METHOD']

    data = '{}'

    matched = match(url.strip('/'), method)
    handler = matched[0]
    route_args = matched[1]

    result = handler(method, route_args, data)

    status = '200 OK'
    headers = [('Content-type', 'application/json')]

    start_response(status, headers)
    return [result.encode('utf-8')]

httpd = make_server('', 8000, front)
print("Serving on port 8000...")
httpd.serve_forever()