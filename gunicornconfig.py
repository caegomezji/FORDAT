import config as cf

import multiprocessing
# listen to port 5858 on all available network interfaces
bind = "{0}:{1}".format(cf.app_host ,cf.app_port )
#bind="192.168.0.15:8080"
# run the app in multiple processes
#workers = 4 if (multiprocessing.cpu_count() * 2 + 1)>=4 else 2 #dice que con 4-12 pueden manejar de cientos a miles de solicitudes deje 4 maxi
workers = cf.kernels
#https://docs.gunicorn.org/en/stable/design.html
#(Always remember, there is such a thing as too many workers. After a point your worker processes will
#start thrashing system resources decreasing the throughput of the entire system. )
worker_class = 'sync'
#logs gunicorn
accesslog = "log/access-logfile.log"
errorlog = "log/error-logfile.log"