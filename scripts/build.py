"""Package the static page as a dependency-free Sites Worker."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output = root / 'dist' / 'server'
output.mkdir(parents=True, exist_ok=True)
assets = {
    '/': {'body': (root / 'index.html').read_text(), 'type': 'text/html; charset=utf-8'},
    '/styles.css': {'body': (root / 'styles.css').read_text(), 'type': 'text/css; charset=utf-8'},
}
worker = 'const assets = ' + json.dumps(assets) + ''';
export default {
  fetch(request) {
    if (!['GET', 'HEAD'].includes(request.method)) {
      return new Response('Method not allowed', {status: 405, headers: {Allow: 'GET, HEAD'}});
    }
    const path = new URL(request.url).pathname;
    const asset = assets[path === '/index.html' ? '/' : path];
    if (!asset) return new Response('Not found', {status: 404});
    return new Response(request.method === 'HEAD' ? null : asset.body, {
      headers: {'Content-Type': asset.type, 'X-Content-Type-Options': 'nosniff'}
    });
  }
};
'''
(output / 'index.js').write_text(worker)
print('Built dist/server/index.js')
