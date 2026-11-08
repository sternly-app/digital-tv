"""Syntax-check the inline <script> in index.html with node. Usage: python3 scripts/check_js.py"""
import re, subprocess, sys, tempfile, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
m = re.search(r"<script>(.*)</script>", html, re.S)
if not m:
    sys.exit("no inline script found")
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
    f.write(m.group(1))
r = subprocess.run(["node", "--check", f.name])
print("SYNTAX_OK" if r.returncode == 0 else "SYNTAX_ERROR")
sys.exit(r.returncode)
