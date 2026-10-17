import json,urllib.request
from pathlib import Path
p=Path(__file__).parent;base=json.loads((p/'live-environment.json').read_text())['url'];get=lambda path:json.load(urllib.request.urlopen(base+'/api/v1/'+path))
a=get('activity');s=get('status');payments=[x for x in a if x['kind']=='send'];assert len(payments)==4
assert sorted(x['amount_zatoshi'] for x in payments)==[1000000,3000000,4000000,5000000]
assert all(x['status']=='confirmed' for x in payments)
transactions={x['txid']:get('transactions/'+x['txid']) for x in payments};assert all(x['confirmations']>0 for x in transactions.values());assert all(transactions[x['txid']]['blockhash']==x['block_hash'] for x in payments)
events=[json.loads(l) for l in (p/'requests.jsonl').read_text().splitlines()];sends=[x for x in events if x['event']=='received' and x['path']=='/api/v1/send'];assert len({json.loads(x['request'])['idempotency_key'] for x in sends})==4
for key in {json.loads(x['request'])['idempotency_key'] for x in sends}:
 group=[x for x in sends if json.loads(x['request'])['idempotency_key']==key]
 assert len({x['request'] for x in group})==1
 assert len({json.loads(x['response'])['id'] for x in group})==1
assert s['settled'];accounts=get('accounts');(p/'live-results.json').write_text(json.dumps({'status':s,'accounts':accounts,'payments':payments,'transactions':transactions,'send_requests':sends,'dropped_responses':[x for x in events if x['event']=='dropped' and x['path']=='/api/v1/send']},indent=2));print(json.dumps({'height':s['node_height'],'payments':[(x['amount_zatoshi'],x['status']) for x in payments],'send_posts':len(sends)},indent=2))
