import hashlib
import re

import requests


class OsirixPortal(object):
    url = r'http://172.17.148.230:3333'

    def __init__(self, id='', pw='', OSID=''):
        self.session = requests.Session()
        self.session.hooks = {'response': lambda r, *args, **kwargs: r.raise_for_status()}
        self.header = {'Referer': r'http://172.17.148.230:3333/', 'Host': '172.17.148.230:3333'}
        self.session.get(OsirixPortal.url)
        self.id = id
        self.pw = pw
        self.OSID = OSID
        if id != '' and pw != '':
            self.login(id, pw)
        if OSID != '':
            self.is_valid(OSID)

    def login(self, id='', pw=''):
        if id == '':
            id = self.id
        if pw == '':
            pw = self.pw
        sh = hashlib.sha1((str(pw) + str(id)).encode('utf-8')).hexdigest()
        self.session.post(OsirixPortal.url,
                          data={'login': '',
                                'username': str(id),
                                'password': str(pw),
                                'sha1': str(sh)},
                          headers=self.header)
        if 'OSID' in self.session.cookies:
            self.OSID = self.session.cookies['OSID']
            return self.OSID
        else:
            return ''

    def is_valid(self, osid=''):
        if osid == '':
            osid = self.OSID
        try:
            r = requests.get('http://172.17.148.230:3333/main',
                             cookies={'OSID': osid},
                             headers=self.header)
        except Exception as e:
            print(e)
            return False
        return (not 'Access to this page is restricted' in r.text)

    def searchAccNo(self, AccNo):
        r = self.session.get(OsirixPortal.url + '/studyList?searchAccessionNumber=' + AccNo,
                             headers=self.header)
        xid_re = re.findall(r'study\?searchAccessionNumber=' + AccNo + '&xid=([\w-]+)', r.text, re.IGNORECASE)
        if xid_re:
            return xid_re[0]
        else:
            return ''

    def deleteStudy(self, AccNo, xid=''):
        if xid == '':
            xid = self.searchAccNo(AccNo)
        url = OsirixPortal.url + '/studyList?searchAccessionNumber=' + AccNo
        r = self.session.post(url,
                              headers={'Referer': url, 'Host': '172.17.148.230:3333'},
                              data={'delete': xid})


if __name__ == '__main__':
    id, pw = 'magic', 'cigamAI'
    os = OsirixPortal(id, pw)
    os.deleteStudy('T0185672408')
