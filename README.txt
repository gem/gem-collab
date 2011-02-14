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

How to start
------------

git clone git@github.com:gem/gem-collab.git
cd GEM/buildout
virtualenv --python=/usr/lib/python2.6 --no-site-packages .
./bin/python2.6 bootstrap.py
./bin/buildout -c start.cfg

./bin/instance fg     # or ./bin/instance start


How to test
-----------

./bin/test -m gem.PACKAGENAME

./bin/testall
