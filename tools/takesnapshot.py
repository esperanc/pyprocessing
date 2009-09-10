#!/usr/bin/env python
"""
This program is used to take snapshots of pyprocessing scripts.

Essentially, it runs a modified version of a given script which
includes a call to save() to be executed after some specified time, 
after which it exits automatically. The snapshot is a .png image
with the same name as the original script.

"""
import sys,re,os.path
from subprocess import Popen,PIPE

#first read the script
if len(sys.argv)<2:
    print "Usage:", sys.argv[0], "pyprocessingscript.py"
    exit (-1)    
try:
    scriptname = sys.argv[1]
    script = open(scriptname).read()
except IOError, (errno, strerror):
    print strerror
    exit(-1)

# compute image name
curdir = os.path.realpath(".")
imagename = curdir+os.sep+os.path.splitext(os.path.split(scriptname)[1])[0]+".png"

# code to be inserted before the run:
snapshotcode = '''

def _takeSnapshot(dt):
    save("'''+imagename+'''")
    print "'''+imagename+''' saved"
    exit(0)
    
pyglet.clock.schedule_once(_takeSnapshot, 1.0)

run()'''

# replace the  "run()" line by the code above
search = re.compile(r"^run\(\)", re.MULTILINE)
doctored_script = search.sub(snapshotcode, script)

python = Popen (["python"], stdin=PIPE)
print>>python.stdin, doctored_script
python.stdin.close()
python.wait()
