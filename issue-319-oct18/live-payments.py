import urllib.request,json,time
from pathlib import Path
p=Path(__file__).parent;base=json.loads((p/'live-environment.json').read_text())['url']
def request(path,body=None):
 req=urllib.request.Request(base+path,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.status,dict(r.headers),json.load(r)
results=[]
for path,body in [('/api/v1/send',{'from_account':1,'to_account':2,'source_pool':'ironwood','destination_pool':'ironwood','amount_zatoshi':1000000,'idempotency_key':'live-319-send-oct18'}),('/api/v1/faucet',{'account_id':3,'pool':'ironwood','amount_zatoshi':1000000,'idempotency_key':'live-319-faucet-oct18'})]:
 code,headers,first=request(path,body);assert code==202,(code,first);assert first['created_at']
 location=next(v for k,v in headers.items() if k.lower()=='location')
 _,_,lookup=request(location);_,_,replay=request(path,body)
 assert len(lookup)==1
 assert first['id']==lookup[0]['id']==replay['id']
 assert first['created_at']==lookup[0]['created_at']==replay['created_at']
 deadline=time.monotonic()+180
 while True:
  _,_,current=request(location)
  if current[0]['status'] in ['confirmed','failed']:break
  assert time.monotonic()<deadline,current
  time.sleep(1)
 assert current[0]['status']=='confirmed',current
 _,_,all_activity=request('/api/v1/activity?limit=100')
 assert sum(x['id']==first['id'] for x in all_activity)==1
 result={'path':path,'initial_status_code':code,'initial':first,'lookup':lookup,'replay':replay,'confirmed':current[0],'single_activity':True}
 results.append(result);(p/'live-payments.json').write_text(json.dumps(results,indent=2))
 print(path,code,first['created_at'],'confirmed',current[0]['txid'],flush=True)
