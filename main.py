import learn

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

api.get_file_list(course_list[3][0])

