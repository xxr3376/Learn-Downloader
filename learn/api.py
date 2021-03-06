#!encoding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import const
import re

class LearnAPI(object):
  def __init__(self):
    self.logined = False
    self.session = requests.Session()
    pass

  def login(self, username, password):
    try:
      payload = {'userid' : username, 'userpass' : password}
      r = self.session.post(const.URL['login'], data=payload)
      r.raise_for_status()

      if re.findall(r'(alert|error)', r.text):
        print 'username or password error!'
        raise Exception('username or password error')
    except:
      return False
    self.logined = True
    return True

  def get_all_course_list(self):
    assert self.logined

    r = self.session.get(const.URL['course_all'])
    r.raise_for_status()

    doc = bs(r.text)

    id_re = re.compile(r'.*\?course_id=(\d*)$')
    name_re = re.compile(r'^(.*)\s*\([^(]*\)\s*\(([^(]*)\)$')
    result = []
    for item in doc.select('#info_1 a'):
      id_ = int(id_re.match(item['href'].strip()).group(1))
      title = item.text.strip()
      name, term = name_re.match(title).groups()
      result.append((id_, name, term))

    return result

  def get_list_template(self, type_, course_id):
    assert self.logined

    r = self.session.get(const.URL[type_], params={"course_id":course_id})
    r.raise_for_status()

    doc = bs(r.text)
    table = doc.find(id='table_box')
    list_ = table.select('.tr1') + table.select('.tr2')

    # return a table
    return map(lambda x:x.find_all('td'), list_)

  def get_file_list(self, course_id):
    dom_list = self.get_list_template('file', course_id)

    result = []

    for tr in dom_list:
      id_ = tr[0].get_text()
      name = tr[1].get_text().strip()
      href = const.URL['base_URL'] + tr[1].find('a')['href']
      result.append((id_, name, href))
    return result

  def download_file(self, url, filename):
    assert self.logined
    r = self.session.get(url, stream=True)

    real_name = r.headers['content-disposition'].decode('gbk', 'replace').split('"')[1]
    real_name = real_name.replace('/', '_')
    real_name = real_name.replace('\\', '_')

    filename = filename + '-' + real_name
    print u'downloading file: %s' % filename

    with open(filename, 'wb') as f:
      for chunk in r.iter_content(1024):
        f.write(chunk)

    return filename
