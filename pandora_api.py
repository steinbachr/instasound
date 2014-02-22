import requests
import pdb


class PandoraApi():
    def __init__(self, username=None, password=None):
        self.base_url = 'http://tuner.pandora.com/services/json/'
        self.username = username
        self.password = password

        self.partner_token = None


    def get_partner_token(self):
        """
        'technically' a crack into pandora's api
        """
        resp = requests.post(self.base_url, data={
            'username': 'android',
            'password': 'AC7IBG09A3DTSYM4R41UJWL07VLN8JI7',
            'deviceModel': 'android-generic',
            'version': '5'
        })
        pdb.set_trace()
        json_resp = resp.json
        return json_resp['result']


pand = PandoraApi()
pand.get_partner_token()