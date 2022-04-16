from decouple import config


dbhost = config('dbhost', default='')
dbdbname = config('dbdbname', default='')
dbuser = config('dbuser', default='')
dbpassword = config('dbpassword', default='')
bottoken = config('bottoken', default='')