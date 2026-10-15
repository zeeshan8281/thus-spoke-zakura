import http from 'node:http';
import fs from 'node:fs';
const dir = '/Users/zeeshan/zakura-281-evidence/live';
const upstream = new URL(JSON.parse(fs.readFileSync(`${dir}/live-environment.json`)).url);
const server = http.createServer((req, res) => {
  const cors = {'access-control-allow-origin':'*','access-control-allow-methods':'GET, POST, OPTIONS','access-control-allow-headers':'content-type'};
  if(req.method === 'OPTIONS') { res.writeHead(204,cors);res.end();return; }
  if(req.url === '/storage-restricted') {
    res.writeHead(200,{'content-type':'text/html',...cors});
    res.end('<!doctype html><html><head><title>Live Regtest - browser storage restricted</title><style>body{margin:0;background:#171717;color:white;font:14px sans-serif}header{padding:12px}iframe{width:100%;height:calc(100vh - 44px);border:0}</style></head><body><header>Live Regtest dashboard. Browser sandbox denies storage. <a style="color:#eaa1b5" href="/">Open with storage allowed</a></header><iframe title="Live Regtest dashboard" sandbox="allow-scripts allow-forms" src="/"></iframe></body></html>');return;
  }
  const requestHeaders={...req.headers,host:upstream.host}; delete requestHeaders.origin;
  const r = http.request({hostname:upstream.hostname,port:upstream.port,path:req.url,method:req.method,headers:requestHeaders}, u => {
    const headers={...u.headers,...cors};delete headers['x-frame-options'];
    res.writeHead(u.statusCode,headers);
    const chunks=[];
    u.on('data', chunk=>{if(req.url !== '/api/v1/events') chunks.push(chunk);});
    u.on('end',()=>fs.appendFileSync(`${dir}/requests.jsonl`,JSON.stringify({time:new Date().toISOString(),method:req.method,path:req.url,status:u.statusCode,body:req.url.startsWith('/api/')?Buffer.concat(chunks).toString():undefined})+'\n'));
    u.pipe(res);
  });
  r.on('error',e=>{res.writeHead(502,cors);res.end(e.message);});
  req.pipe(r);
});
server.listen(59182,'127.0.0.1',()=>console.log('http://127.0.0.1:59182'));
