import time
from fabric.api import run, execute, env

environment = "production"

env.use_ssh_config = True
env.hosts = ["search"]

branch = "master"
repo = "git@github.com:18f/foia-search.git"

username = "foia"
home = "/home/foia/search"
shared_path = "%s/shared" % home
versions_path = "%s/versions" % home
version_path = "%s/%s" % (versions_path, time.strftime("%Y%m%d%H%M%S"))
current_path = "%s/current" % home

# how many old releases to be kept at deploy-time
keep = 10

# port in the storm
port = 3000

# can be run only as part of deploy
def checkout():
  run('git clone -q -b %s %s %s' % (branch, repo, version_path))

def links():
  run("ln -s %s/config.js %s/config/config.js" % (shared_path, version_path))

# install node and python dependencies
def dependencies():
  run("cd %s && npm install && pip install -r requirements.txt" % version_path)

# TODO: why cp instead of ln?
def make_current():
  run('rm -rf %s && cp -r %s %s' % (current_path, version_path, current_path))

def cleanup():
  versions = run("ls -x %s" % versions_path).split()
  # destroy all but the most recent X
  destroy = versions[:-keep]

  for version in destroy:
    command = "rm -rf %s/%s" % (versions_path, version)
    run(command)


## can be run on their own
#
# but fabric is not working, until then -
#
# to run on server:
#   cd /home/foia/search/current && NODE_ENV=production forever -l /home/foia/search/shared/log/forever.log -a start app.js -p 3000
#
# and to stop on server:
#   forever stop app.js -p 3000
#
# and to restart on server:
#   forever restart app.js -p 3000
def start():
  run("cd %s && NODE_ENV=%s forever -l %s/log/forever.log -a start app.js -p %i" % (current_path, environment, shared_path, port))

def stop():
  run("forever stop app.js -p %i" % port)

def restart():
  run("forever restart app.js -p %i" % port)

def deploy():
  execute(checkout)
  execute(links)
  execute(dependencies)
  execute(make_current)
  execute(restart)
  execute(cleanup)

def deploy_cold():
  execute(checkout)
  execute(links)
  execute(dependencies)
  execute(make_current)
  execute(start)
