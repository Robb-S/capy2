import sys, os
INTERP = '/home/lobsterinc/capybara.animalcafes.com/capyenv/bin/python3.6'
if sys.executable != INTERP:
	os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from capy import app as application

