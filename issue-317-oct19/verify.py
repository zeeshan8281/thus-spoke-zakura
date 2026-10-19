import json,urllib.request
from pathlib import Path
p=Path(__file__).parent;base=json.loads((p/'observer.json').read_text())['url']
def get(path):return json.load(urllib.request.urlopen(base+'/api/v1/'+path))
a=json.loads((p/'clock-before.json').read_text());b=json.loads((p/'clock-after.json').read_text());requests=[json.loads(l) for l in (p/'requests.jsonl').read_text().splitlines()]
activity_requests=[r for r in requests if a['at']<=r['at']<=b['at'] and r['path'].startswith('/api/v1/activity')]
assert not activity_requests,activity_requests
assert a['times'][0]['text']!=b['times'][0]['text']
assert [(t['dateTime'],t['title']) for t in a['times']]==[(t['dateTime'],t['title']) for t in b['times']]
assert a['rows'][1]==b['rows'][1] and 'Block 106' in b['rows'][1]
activity=get('activity');unknown=[x for x in activity if x['created_at'] is None];assert len(unknown)==1 and unknown[0]['mined_height']==106
assert unknown[0]['amount_zatoshi']==2000000
assert all(x['status']=='confirmed' for x in activity)
txs={x['txid']:get('transactions/'+x['txid']) for x in activity}
for x in activity:
 assert txs[x['txid']]['confirmations']>0
 assert txs[x['txid']]['blockhash']==x['block_hash']
status=get('status');assert status['settled'];assert status['node_height']==status['lightwalletd_height']==status['wallet_scanned_height']==107
result={'before':a,'after':b,'activity_requests_during_interval':activity_requests,'activity':activity,'transactions':txs,'status':status,'accounts':get('accounts')}
(p/'live-results.json').write_text(json.dumps(result,indent=2));print('PASS:',a['times'][0]['text'],'->',b['times'][0]['text'],'; Block 106 unchanged; no activity GETs; all transactions confirmed; height 107')
