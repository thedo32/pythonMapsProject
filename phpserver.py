from wsgiref.simple_server import make_server
from wfastcgi import Request, wsgiserver

# Assuming your PHP-FPM server is listening on 127.0.0.1:9000
ADDRESS = ('127.0.0.1', 9000)

def application(environ, start_response):
    # Extract PHP script path from request (modify based on your URL structure)
    script_path = environ['PATH_INFO']

    # Create FastCGI request object
    fcgi_request = Request()
    fcgi_request.setBasicHeader('SCRIPT_FILENAME', script_path)

    # Connect to FastCGI server and send request
    with wsgiserver.WSGIServer(ADDRESS, application) as httpd:
        print("Serving at port", httpd.server_port)
        httpd.serve_forever()