from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from job_sources import fetch_linkedin_guest_jobs

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/dashboard.html"
        return super().do_GET()

if __name__ == "__main__":
    print("Open http://127.0.0.1:5557")
    ThreadingHTTPServer(("127.0.0.1", 5557), Handler).serve_forever()
