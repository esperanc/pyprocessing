This project provides a [Python](http://www.python.org) package that creates an environment for graphics applications that closely resembles that of the [Processing](http://www.processing.org) system. [Usage](UsageInstructions.md) is mostly restricted to importing the package and calling `run()`.
For instance, this simple example taken from a [Processing tutorial](http://www.processing.org/learning/drawing) can be ported to pyprocessing as follows:

<table>
<tr>
<td>
<img src='http://www.processing.org/learning/drawing/imgs/1.11.jpg' />
</td>
<td>
<pre><code>// <br>
// Processing <br>
//<br>
size(200,200);<br>
rectMode(CENTER);<br>
rect(100,100,20,100);<br>
ellipse(100,70,60,60);<br>
ellipse(81,70,16,32); <br>
ellipse(119,70,16,32); <br>
line(90,150,80,160);<br>
line(110,150,120,160);<br>
</code></pre>
</td>
<td>
<pre><code>#<br>
# pyprocessing equivalent<br>
#<br>
from pyprocessing import *<br>
size(200,200)<br>
rectMode(CENTER)<br>
rect(100,100,20,100)<br>
ellipse(100,70,60,60)<br>
ellipse(81,70,16,32) <br>
ellipse(119,70,16,32) <br>
line(90,150,80,160)<br>
line(110,150,120,160)<br>
run()<br>
</code></pre>
</td>
</tr>
</table>


The project mission is to implement Processing's friendly graphics functions and interaction model in Python. Not all of Processing is to be ported, though, since Python itself already provides alternatives for many features of Processing, such as XML parsing.

The **pyprocessing** backend is built upon [OpenGL](http://www.opengl.org) and [Pyglet](http://www.pyglet.org), which provide the actual graphics rendering. Since these are multiplatform, so is **pyprocessing**.

We hope that, much in the same spirit of the Processing project, **pyprocessing** will appeal to people who want to easily program and interact with computer generated imagery. It is also meant to help teaching computer programming by making it possible to write compact code with rich visual semantics.