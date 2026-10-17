import json, urllib.request, time
from pathlib import Path
p=Path(__file__).parent
base=json.loads((p/'live-environment.json').read_text())['url']
def get(path):return json.load(urllib.request.urlopen(base+'/api/v1/'+path,timeout=30))
payments=json.loads((p/'live-payments.json').read_text())
transactions={x['confirmed']['txid']:get('transactions/'+x['confirmed']['txid']) for x in payments}
for x in payments:
 a=x['confirmed'];t=transactions[a['txid']]
 assert t['confirmations']>0 and t['blockhash']==a['block_hash']
ui=[x for x in get('activity') if x['kind']=='send' and x['amount_zatoshi']==2000000]
assert len(ui)==1 and ui[0]['status']=='confirmed',ui
t=get('transactions/'+ui[0]['txid']);assert t['confirmations']>0 and t['blockhash']==ui[0]['block_hash']
transactions[ui[0]['txid']]=t
status=get('status')
assert status['settled'],status
(p/'chain-results.json').write_text(json.dumps({'status':status,'accounts':get('accounts'),'transactions':transactions,'activity':get('activity')},indent=2))
print(json.dumps({'height':status['node_height'],'confirmed_transactions':len(transactions),'settled':status['settled']}))
