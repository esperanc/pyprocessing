#!/usr/bin/env python
"""
Usage: takesnapshot.py [options] script.py

This program is used to take snapshots of a pyprocessing 
application called script.py.

Essentially, it runs a modified version of the given script which
includes a call to save(). Command line arguments select one
of the two supported modes of operation:

   --single=<time> : means that the script waits <time> seconds
        before taking a snapshot and then exits. This is the default
        with <time> equal to 1.0 seconds;
        
   --interactive: a snapshot is take each time the F1 key is hit
        but otherwise does not affect the script.

The snapshot is a .png image which, by default, has the same
name as the original script and is stored in the current dir.
If operating in interactive mode, the snapshot names are suffixed
with the number of the take. Thus, the first snapshot of a
script named myscript.py will be called myscript001.png.
"""
import sys,re,os.path,getopt
from subprocess import Popen,PIPE

def usage():
    """Prints usage instructions"""
    print __doc__

# default operation mode
mode = 'single'
time = 1.0


# analyze command line arguments
try:
    opts,args = getopt.getopt(sys.argv[1:], "", ["single=", "interactive"])
except getopt.GetoptError, err:
    # print help information and exit:
    print "Command line error"
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)


for o,a in opts:
    if o == '--single':
        try:
            time = float(a)
        except:
            print "Error: time must be a positive floating point number"
            usage()
            sys.exit(2)
        
    elif o == "--interactive":
        mode = 'interactive'

#first read the script
if len(args)!=1:
    print args
    print "Must give the name of a valid pyprocessing script file"
    usage()
    exit (-1)
    
try:
    scriptname = args[0]
    script = open(scriptname).read()
except IOError, (errno, strerror):
    print "IO error while reading",scriptname
    print strerror
    usage()
    exit(-1)

# compute image name
curdir = os.path.realpath(".")
imagename = curdir+os.sep+os.path.splitext(os.path.split(scriptname)[1])[0]

# codes to be inserted before the run:
singlecode = '''
def _takeSnapshot(dt):
    save("'''+imagename+'''.png")
    print "'''+imagename+'''.png saved"
    exit(0)
    
pyglet.clock.schedule_once(_takeSnapshot, '''+str(time)+''')

run()'''

interactivecode = '''
    
def _installTakeSnapshot(dt):
    def on_key_press(symbol,modifiers):
        if symbol!=F1: return
        global _snapNumber
        _snapNumber += 1
        imgname = "'''+imagename+'''"+"%03d"%_snapNumber+".png"
        save(imgname)
        print imgname+" saved"

    global _snapNumber
    _snapNumber = 0
    canvas.window.push_handlers(on_key_press)
    
pyglet.clock.schedule_once(_installTakeSnapshot, 0.2)

run()
'''

if mode=='single':
    snapshotcode = singlecode
else:
    snapshotcode = interactivecode
    
# replace the  "run()" line by the code above
search = re.compile(r"^run\(\)", re.MULTILINE)
doctored_script = search.sub(snapshotcode, script)

python = Popen (["python"], stdin=PIPE)
print>>python.stdin, doctored_script
python.stdin.close()
python.wait()

