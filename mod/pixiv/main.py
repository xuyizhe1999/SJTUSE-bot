import utils
import requests
import json


def OnMessage(msg):
    if msg['type'] == 'GroupMessage' and (2 <= len(msg['messageChain']) <= 3) and msg['messageChain'][1]['type'] == 'At' and msg['messageChain'][1]['target'] == utils.qqNumber:
        if len(msg['messageChain']) == 2 or (len(msg['messageChain']) == 3 and msg['messageChain'][2]['type'] == 'Plain'and msg['messageChain'][2]['text'] == ' '):
            group = msg['sender']['group']['id']
            r = requests.get(
                'https://api.lolicon.app/setu/', params={
                    'apikey': '522605455f0c66a4a242d8',
                    'size1200': 'true',
                    'r18': 0,
                })
            if r.status_code != 200:
                utils.TryPost('/sendGroupMessage', {
                    'target': group,
                    'messageChain': [
                        {'type': 'Plain', 'text': '涩图暂不可用，多运动少冲！'},
                    ]
                })
                print('[pixiv] send fail status', r.status_code)
                return
            r = json.loads(r.text)
            if r['code'] == 0:
                r = utils.UploadURL(r['data'][0]['url'], 'group')
                print(r)
                utils.TryPost('/sendGroupMessage', {
                    'target': group,
                    'messageChain': [
                        {'type': 'Image', 'imageId': r['imageId']},
                    ]
                })
                print('[pixiv] send')
            else:
                utils.TryPost('/sendGroupMessage', {
                    'target': group,
                    'messageChain': [
                        {'type': 'Plain', 'text': '涩图暂不可用，多运动少冲！'},
                    ]
                })
                print('[pixiv] send fail code', r['code'])