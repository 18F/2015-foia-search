### Deploying

What I did to get this working on the dev server so far, based off of a proposed 0.1.3 AMI.

**Elasticsearch**

* Installed Java 7 (`apt-get install openjdk-7-jre`)
* Added the elasticsearch apt repository and its PGP key.
* Installed elasticsearch 1.2.2 from it, and enabled elasticsearch on boot.
* Customized the elasticsearch config file (preserved in config/server/dev.yml)
* Started elasticsearch.

**Node**

* Downloaded Node from its homepage with wget.
* Moved it to `/opt/install`.
* Compiled it from source and installed system-wide.

**Python**

* Installed `pyenv` to `/opt/install/pyenv`.
* Installed the `pyenv-virtualenvwrapper` plugin.
* Installed 3.4.0, and set as global and default.
* Enabled `pyenv` and `pyenv-virtualenvwrapper` in the `.bashrc` for `ubuntu` and `foia`.
* Made `/opt/virtualenvs/foia` and gave `foia` ownership of it.
* Set `$WORKON_HOME` to `/opt/virtualenvs/foia` for `foia`.

**Project configuration**

* Removed the default nginx vhost and made `/etc/nginx/vhosts/foia.conf`, reverse proxying to localhost:3000.
* Cloned `foia` and `foia-search` to the `foia` user's home dir.
* Made a place for nginx logs there.
* Installed `pdftotext` via `apt-get poppler-utils`.
* Froze scrapelib to 0.9.1, need to update state scraper.
* Created a `foia` index and `PUT` the documents mapping to it.
* Downloaded a few pages of State department data.
* Indexed those downloaded documents (~36).
* Restarted node app server.

**When setting up foia-core**

* Updated to Python 3.4.1, installed virtualenvwrapper.
* `apt-get install postgres` for using Postgres
* created `foia` database and added username/pass `foia`/`foia`
* `apt-get install libpq-dev postgres-server-dev-9.3` for building Python pg
* Updated foia-search virtualenv to use `3.4.1`
* Updated `.bashrc` with `PYTHONPATH` and `DJANGO_SETTINGS_MODULE`
* Fixed virtualenvwrapper error by adding `VIRTUALENVWRAPPER_HOOK_DIR` to `.bashrc`
* Cloned foia-core repo to `~foia/core/current` and put logs at `~foia/core/search`
* Ran `syncdb`, created `foia` superuser with pass `foia`
* Loaded scraped FOIA contact YAML into database with `load_agency_contacts.py`
* Added new vhost at `/etc/nginx/vhosts/core.conf` that proxies to `localhost:8000`
* Pointed `core` and `search` vhosts to server names of `http://foia-core` and `http://foia-search` respectively, updating `/etc/hosts` is needed to visit them

**For the next server**

* Use 0.1.4 instead.
* Freeze Java 7 into AMI ahead of time (so maybe 0.1.5).
* Install Python libs ahead of time: `apt-get install libbz2-dev libreadline-dev libsqlite3-dev`
* Move elasticsearch index to its own dedicated EBS directory.
* Configure elasticsearch to point to other dirs (like its work dir to `/tmp`).
* Update scrapelib to 0.10.1 in state scraper.
* Get fabric working correctly.
* Tie in the repo's version controlled ES config and nginx vhost into what they depend on.


### server config

`.bashrc` head:

```bash
# foia-core
export DJANGO_SETTINGS_MODULE=foia_core.settings.dev
export PYTHONPATH=/home/foia/core/current:PYTHONPATH

# pyenv bin
export PYENV_ROOT=/opt/install/pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
pyenv virtualenvwrapper

# home dir for virtualenvs for foia
export WORKON_HOME=/opt/virtualenvs/foia
export VIRTUALENVWRAPPER_HOOK_DIR=/opt/virtualenvs/foia
```