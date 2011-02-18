GEM
---

To clone the repo just:

* Register on github.com
* Put your ssh public key on github
* Ask to marcom@openquake.org to add your user to the private repository

git clone git@github.com:gem/gem-collab.git

...make changes...

git add file # if it's a new file
git commit -a -m "commit message" # commit to the local repo
git push origin master # push your changes to the remote repo


* To pull (get the changes) just:

git pull

* If you generate files that are not related to the repository (for example
  output of tests) you could do:

git clean -n # just to see what files are going to be removed
git clean -f # to *really* remove the files

How to start (with virtualenv -- not really tested)
---------------------------------------------------

git clone git@github.com:gem/gem-collab.git
cd GEM/buildout
virtualenv --python=/usr/bin/python2.6 --no-site-packages .
./bin/python2.6 bootstrap.py
./bin/buildout -c start.cfg



How to start (with the Unified Installer)
---------------------------------------------------


wget http://launchpad.net/plone/4.0/4.0.3/+download/Plone-4.0.3-20110720-UnifiedInstaller.tgz
tar xfz Plone-4.0.3-20110720-UnifiedInstaller.tgz 
cd Plone-4.0.3-UnifiedInstaller/
./install.sh standalone # This takes a while

After plone is installed under your $HOME/Plone
cd $HOME/Plone/zinstance/
ln -s /your/git/repo/location/buildout/config.d .
cd src
ln -s /your/git/repo/location/modules/yourmodule . # for example gem.community
cd ..

create a start.cfg file inside the $HOME/Plone/zinstance dir containing:

[buildout]
extends = config.d/devel.cfg

then execute:

export C_INCLUDE_PATH=/usr/include/tcl8.5 # or your tcl location
./bin/buildout -c start.cfg # this takes a while too :)


How to run
----------

./bin/instance fg     # or ./bin/instance start

How to test
-----------

./bin/test -m gem.PACKAGENAME

./bin/testall
