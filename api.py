__author__ = 'powergx'
import json
import requests
from crysadm_helper import r_session
from requests.adapters import HTTPAdapter

requests.packages.urllib3.disable_warnings()


def exec_draw_cash(cookies):
    r = get_drawcash_info(cookies)
    if r.get('r') != 0:
        return r
    if r.get('is_tm') == 0:
        return dict(r=0, rd=r.get('tm_tip'))
    """
    可以提现就提，不然返回错误信息。
    """
    r = get_balance_info(cookies)
    if r.get('r') != 0:
        return r
    wc_pkg = r.get('wc_pkg')
    if wc_pkg > 200:
        wc_pkg = 200

    r = draw_cash(cookies, wc_pkg)
    if r.get('r') != 0:
        return r

    return r


def draw_cash(cookies, m):
    """
    提现
    :param cookies:
    :return:
    """
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '2'

    body = dict(hand='0', m=str(m), v='3', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=usr/drawpkg', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_drawcash_info(cookies):
    """
    是否可以提现
    {"r":0,"rd":"ok","is_tm":1,"is_bd":1,"tm_tip":"\u63d0\u73b0\u5f00\u653e\u65f6\u95f4\u4e3a\u6bcf\u5468\u4e8c11:00-18:00(\u56fd\u5bb6\u6cd5\u5b9a\u8282\u5047\u65e5\u9664\u5916)","draw_flag":1}
    :param cookies:
    :return:
    """
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '2'

    body = dict(hand='0', v='1', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=usr/drawcashInfo', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_balance_info(cookies):
    "获取余额"
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '2'

    body = dict(hand='0', v='2', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=usr/asset', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_can_drawcash(cookies):
    "获取余额"
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '2'

    body = dict(hand='0', v='1', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=usr/drawcashInfo', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_income_info(cookies):
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '1'
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.get('https://red.xunlei.com/?r=usr/getinfo&v=1', verify=False, cookies=cookies,
                         headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_mine_info(cookies):
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '1'
    body = dict(hand='0', v='2', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=mine/info', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_speed_stat(s_type, cookies):
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '1'
    body = dict(type=s_type, hand='0', v='0', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=mine/speed_stat', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        __handle_exception(e=e)
        return [0] * 24
    if r.status_code != 200:
        __handle_exception(rd=r.reason)
        return [0] * 24
    return json.loads(r.text).get('sds')


def get_privilege(cookies):
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '1'
    body = dict(hand='0', v='0', ver='1')
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.post('https://red.xunlei.com/?r=usr/privilege', data=body, verify=False, cookies=cookies,
                          headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_device_stat(s_type, cookies):
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '1'
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    url = 'https://red.xunlei.com/?r=mine/devices_stat'

    body = dict(type=s_type, hand='0', v='2', ver='1')
    this_cookies = cookies.copy()
    if len(this_cookies.get('sessionid')) != 128:
        this_cookies['origin'] = "2"
    try:
        r = requests.post(url=url, verify=False, data=body, cookies=this_cookies,
                          headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def collect(cookies):
    if len(cookies.get('sessionid')) == 128:
        cookies['origin'] = '4'
    else:
        cookies['origin'] = '1'
    headers = {'user-agent': "RedCrystal/1.5.0 (iPhone; iOS 8.4; Scale/2.00)"}
    try:
        r = requests.get('https://red.xunlei.com/index.php?r=mine/collect', verify=False, cookies=cookies,
                         headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def get_device_info(user_id):
    url = 'http://webmonitor.dcdn.sandai.net/query_device?USERID=%s' % user_id
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        r = s.get(url, verify=False, timeout=10)
    except requests.exceptions.RequestException as e:
        return __handle_exception(e=e)
    if r.status_code != 200:
        return __handle_exception(rd=r.reason)
    return json.loads(r.text)


def is_api_error(r):
    if r.get('r') == -12345:
        return True
    return False


def __handle_exception(e=None, rd='接口故障', r=-12345):
    if e is None:
        print(rd)
    else:
        print(e)

    b_err_count = r_session.get('api_error_count')
    if b_err_count is None:
        r_session.setex('api_error_count', '1', 60)
        return dict(r=r, rd=rd)

    err_count = int(b_err_count.decode('utf-8')) + 1

    if err_count > 200:
        r_session.setex('api_error_info', '迅雷矿场API故障中,攻城狮正在赶往事故现场,请耐心等待.', 60)

    err_count_ttl = r_session.ttl('api_error_count')
    if err_count_ttl is None:
        err_count_ttl = 30
    r_session.setex('api_error_count', str(err_count), err_count_ttl + 1)
    return dict(r=r, rd=rd)
