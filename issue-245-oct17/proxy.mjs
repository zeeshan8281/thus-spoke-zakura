import http from 'node:http';
import fs from 'node:fs';
const dir='/Users/zeeshan/zakura-275-oct17';
const upstream=new URL(JSON.parse(fs.readFileSync(`${dir}/live-environment.json`)).url);
const log=(item)=>fs.appendFileSync(`${dir}/requests.jsonl`,JSON.stringify({at:new Date().toISOString(),...item})+'\n');
http.createServer((req,res)=>{
 const request=[];req.on('data',c=>request.push(c));
 const r=http.request({hostname:upstream.hostname,port:upstream.port,path:req.url,method:req.method,headers:{...req.headers,host:upstream.host}},u=>{
  if(req.url==='/api/v1/events'){res.writeHead(u.statusCode,u.headers);u.pipe(res);return;}
  const chunks=[];u.on('data',c=>chunks.push(c));u.on('end',()=>{
   const data=Buffer.concat(chunks);
   const item={method:req.method,path:req.url,status:u.statusCode,request:Buffer.concat(request).toString(),response:req.url.startsWith('/api/')?data.toString():undefined};
   const kind=req.url==='/api/v1/send/quote'?'quote':req.url==='/api/v1/send'?'send':null;
   log({event:'received',...item});
   const deliver=()=>{
    if(kind&&fs.existsSync(`${dir}/hold-${kind}`)){setTimeout(deliver,100);return;}
    if(kind&&fs.existsSync(`${dir}/drop-${kind}`)){log({event:'dropped',...item});res.destroy();return;}
    res.writeHead(u.statusCode,u.headers);res.end(data);log({event:'delivered',...item});
   };deliver();
  });
 });r.on('error',e=>{log({event:'transport-error',path:req.url,error:e.message});res.destroy();});req.pipe(r);
}).listen(59183,'127.0.0.1',()=>console.log('http://127.0.0.1:59183'));
