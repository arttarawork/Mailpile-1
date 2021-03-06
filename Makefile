# Recipies for stuff
export PYTHONPATH := .

all:	docs alltests dev

dev:
	@echo export PYTHONPATH=`pwd`

docs:
	python mailpile/urlmap.py >doc/URLS.md
	python mailpile/defaults.py |grep -v ';timestamp' >doc/defaults.cfg

alltests:
	python mailpile/config.py \
	&& python mailpile/util.py \
	&& python mailpile/workers.py \
	&& scripts/mailpile-test.py \

clean:
	@rm -vf *.pyc */*.pyc */*/*.pyc mailpile-tmp.py mailpile.py
	@rm -vf .appver MANIFEST setup.cfg .SELF
	@rm -vrf *.egg-info build/ mp-virtualenv/ dist/

virtualenv:
	virtualenv mp-virtualenv
	bash -c 'source mp-virtualenv/bin/activate && pip install -r requirements.txt && python setup.py install'
	
