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

**For the next server**

* Use 0.1.4 instead.
* Freeze Java 7 into AMI ahead of time (so maybe 0.1.5).
* Install Python libs ahead of time: `apt-get install libbz2-dev libreadline-dev libsqlite3-dev`
* Move elasticsearch index to its own dedicated EBS directory.
* Configure elasticsearch to point to other dirs (like its work dir to `/tmp`).
* Update scrapelib to 0.10.1 in state scraper.
* Get fabric working correctly.