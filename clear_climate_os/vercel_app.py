from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Streamlit app deployed. Please note: Streamlit requires WebSockets which are not natively supported by Vercel Serverless Functions.'.encode('utf-8'))
        return

app = handler
