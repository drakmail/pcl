from fabric.api import *

env.hosts = ["pztrn@urtrussia.org"]
env.port = "9900"
env.directory = "/data/WWW/league.urtrussia.org/public/"

def deploy():
    with settings(warn_only=True):
        with cd(env.directory):
            if run("test -f {0}/index.py".format(env.directory)).failed:
                run("git clone git://git.urtrussia.org/pcl.git .")
            else:
                run("git pull")
            run("chmod +x index.py")
            run("./wsgi_mode.sh restart")

def restart():
    with settings(warn_only=True):
        with cd(env.directory):
            run("./wsgi_mode.sh restart")

def stop():
    with settings(warn_only=True):
        with cd(env.directory):
            run("./wsgi_mode.sh stop")

def start():
    with settings(warn_only=True):
        with cd(env.directory):
            run("./wsgi_mode.sh start")