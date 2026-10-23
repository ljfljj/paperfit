# -*- coding: utf-8 -*-
"""PaperFit Web：python serve.py → http://127.0.0.1:8000"""
import cgi, cgitb, json, os, sys, tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperfit.checker import check
from paperfit.report import render

BASE = os.path.dirname(os.path.abspath(__file__))
RULES = json.load(open(os.path.join(BASE, "rules", "dazuoye.json"), encoding="utf-8"))
INDEX = os.path.join(BASE, "web", "index.html")

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, open(INDEX, encoding="utf-8").read())
        else:
            self._send(404, "not found")

    def do_POST(self):
        cgitb.enable(display=0, logdir=None)
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={"REQUEST_METHOD": "POST"})
        item = form["file"] if "file" in form else None
        if item is None or not getattr(item, "filename", ""):
            return self._send(400, "<h3>没有收到文件</h3>")
        suffix = os.path.splitext(item.filename)[1] or ".docx"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(item.file.read())
        tmp.close()
        try:
            res = check(tmp.name, RULES)
            res["file"] = item.filename
            out = tmp.name + ".html"
            render(res, out)
            self._send(200, open(out, encoding="utf-8").read())
        except Exception as e:
            self._send(500, f"<h3>解析失败</h3><pre>{e}</pre>")
        finally:
            for p in (tmp.name, tmp.name + ".html"):
                try: os.unlink(p)
                except Exception: pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"PaperFit Web 已启动： http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), H).serve_forever()
