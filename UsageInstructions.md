# Writing a pyprocessing application #

Pyprocessing works in much the same fashion as [Processing](http://www.processing.org). In fact, most functions in pyprocessing mimic the equivalent Processing functions to the letter. If you are familiar with Processing and Python, you already know almost everything you need to write pyprocessing applications. To cut a long story short, the only thing you need to do is to _import_ the pyprocessing package, write the rest of your code using pyprocessing functions and data structures, and call `run()`.

## Simple usage ##

Unlike [Processing](http://www.processing.org), pyprocessing is not a full fledged IDE but
merely a Python package. Thus, you must use your favorite text editor or Python
IDE to write a regular Python program which imports the pyprocessing package. We suggest
doing it at the beginning of your application:

```
from pyprocessing import *
```

After the import, a default 100x100 pixel window is defined, on which the application may now draw using pyprocessing functions and other Python commands. For instance:

```
smooth()
for i in range(10):
    line(i*5+5,20,i*5+50,80)
```

The last instruction should be a call to the `run()` function:

```
run()
```

When this line is reached, the graphics window, which was hidden until this point, will finally be shown and the application
will enter the event dispatching loop. In principle, `run()` does not return, but
you can terminate the application by typing the `ESC` key.

In case you're wondering, here's the complete script and the contents of the drawing:

<table>
<tr>
<td>

<img src='http://pyprocessing.googlecode.com/svn/wiki/UsageInstructions.figs/basicusage.png' />

</td>
<td>
<pre><code>from pyprocessing import *<br>
<br>
smooth()<br>
for i in range(10):<br>
    line(i*5+5,20,i*5+50,80)<br>
<br>
run()<br>
</code></pre>
</td>
</tr>
</table>

## Changing the default window ##

As with Processing, the window size may be changed with the `size()` function.
It has two required arguments: the width and height of the desired window in
pixels. Thus,
```
size(200,200)
```
will open a 200x200 pixels window.

By default, pyprocessing windows are not resizable, since this is the
expected Processing behavior. You can, however, request a resizable window by
adding the keyword argument `resizable=True`:
```
size(200,200,resizable=True)
```
It is even possible to request a full screen window by using the keyword argument
`fullscreen=True`.

Pyprocessing will adjust the coordinate system to reflect the changed window
dimensions. Thus, if the window is resized so that it is now 250 pixels wide
and 150 pixels high, the pixels will be addressed by _x_ in interval [0, 250) and
_y_ in interval [0, 150), where pixel (0,0) is the top left corner of
the window, i.e., the _y_ axis points _down_.

Of course, if the window is resized, the original contents drawn so far will
be lost, and pyprocessing will automatically call the `draw()` function
you defined in your program, if any (see the next section).


## Animation ##

In order to do animations or to deal with resizing windows, the application must define a callback function called `draw()`. By default, `draw()` is called continuously 60 times per second.

Pyprocessing also supports the `setup()` callback convention, i.e., if you define a function called `setup()`, it will be called exactly once by `run()`. Notice that in Processing, so called _static_ programs -- or _sketches_ in Processing parlance -- do not define any functions (callbacks or otherwise), while the initialization of a program with a `draw()` is almost always performed by `setup()`. On the other hand, pyprocessing is less strict, i.e., you can put initialization code inside a `setup()` function or directly in the main program regardless of whether a `draw()` callback function was defined or not.

In the example below, which implements an animation with two balls, `setup()` is automatically called once to initialize the screen and some drawing modes, whereas `draw()` is called repeatedly to update the `balls` array and draw the frame.

<table>
<tr>
<td>

<img src='http://pyprocessing.googlecode.com/svn/wiki/UsageInstructions.figs/animation001.png' />

<img src='http://pyprocessing.googlecode.com/svn/wiki/UsageInstructions.figs/animation004.png' />

<img src='http://pyprocessing.googlecode.com/svn/wiki/UsageInstructions.figs/animation007.png' />

</td>
<td>
<pre><code>from pyprocessing import *<br>
<br>
balls = [(20,20,2.5,3,10),(100,50,-3.5,-3,15)]<br>
<br>
def setup():<br>
    size(150,150)<br>
    ellipseMode(CENTER)<br>
    noStroke()<br>
<br>
def draw():<br>
    fill(200,50)<br>
    rect(0,0,150,150)<br>
    fill(0)<br>
    for i in range(len(balls)):<br>
        x,y,dx,dy,r = balls[i]<br>
        x += dx<br>
        if constrain(x,r,150-r) != x: dx = -dx<br>
        y += dy<br>
        if constrain(y,r,150-r) != y: dy = -dy<br>
        balls[i] = x,y,dx,dy,r<br>
        ellipse(x,y,r,r)<br>
<br>
run()<br>
</code></pre>
</td>
</tr>
</table>

## Interaction ##

An interactive application must process user input such as mouse clicks or keyboard typing. Again, following Processing's practice, the state of input devices is kept in _global_ variables which can either be polled in your `draw()` function or queried only when their value changes by means of callback functions.

The example program shown below illustrates a simple scribbling application where dragging the mouse paints freehand lines and hitting the 'C' key clears the screen.

<table>
<tr>
<td>
<img src='http://pyprocessing.googlecode.com/svn/wiki/UsageInstructions.figs/interactioncallback001.png' />
</td>
<td>
<pre><code>from pyprocessing import *<br>
<br>
size(200,200)<br>
<br>
def draw():<br>
    # scribble a line with the mouse<br>
    if mouse.pressed:<br>
        line (pmouse.x, pmouse.y, mouse.x, mouse.y)<br>
    # typing 'C' clears the screen<br>
    if key.pressed and key.char in 'cC':<br>
        background(200)<br>
<br>
run()<br>
</code></pre>
</td>
</tr>
</table>

The same application can be rewritten in a more efficient manner by using callback functions:

```
from pyprocessing import *

size(200,200)

def mouseDragged():
    # scribble a line with the mouse
    line (pmouse.x, pmouse.y, mouse.x, mouse.y)
    
def keyPressed():
    # typing 'C' clears the screen
    if key.char in 'cC':
        background(200)

run()
```

### A note about state variables ###

Due to the characteristics of the Python language, pyprocessing uses a naming for state variables that is slightly different from the one used by Processing. For instance, whereas Processing uses the boolean variable `mousePressed` to tell whether or not a mouse button is pressed, the equivalent variable in pyprocessing is named `mouse.pressed`. The reason for this is that Java -- the actual programming language that underlies Processing -- allows identifiers to be overloaded and thus it is perfectly alright to have a variable named `mousePressed` and a function called `mousePressed()` while in Python this is not allowed.