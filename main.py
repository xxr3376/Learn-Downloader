import learn
import distutils.dir_util

try:
  import secret
except:
  pass

api = learn.api()

if secret:
  username = secret.username
  password = secret.password
else:
  # ask for username and password
  pass

if not api.login(username, password):
  print 'login failed'

course_list = api.get_all_course_list()

for course_id, course_name, term in course_list:
  file_list = api.get_file_list(course_id)
  course_path = 'data/%s/%s-%s' % (term, course_id, course_name)
  distutils.dir_util.mkpath(course_path)

  distutils.dir_util.mkpath(course_path + '/file/')

  relation = []
  for file_id, filename, file_link in file_list:
    filename = filename.replace('/', '_')
    filename = filename.replace('\\', '_')

    file_path = "%s/file/%s" % (course_path, file_id)

    real_path = api.download_file(file_link, file_path)

    relation.append( "%s\t%s" % (real_path.split('/')[-1], filename))
  with open(course_path + '/file/relation.tsv', 'wb') as f:
    f.write('\n'.join(relation).encode('utf-8'))
