# Configuration files #

Pyprocessing users may set personal preferences in two context levels, a global
context and a 'per user' context.
These preferences are stored as plain text files which can be easily changed with a text editor. Preferences are nested, meaning that you can have some preferences set globally and others in an user context which supersede the global preferences.

Global Context: Having more priority than the default values but less than the user's, the Global Context preferences can be stored in a globalconfig.txt file inside the pyprocessing installation folder. Notice that you must have administration privileges to modify this file.

User Context: Has the highest priority and can be stored in a file called `userconfig.txt` stored inside the _homepath_/`.pyprocessing` folder. Like the `globalconfig.txt`, it isn't created by default and uses the same template. The _homepath_ is the user's home folder, which is normally set as `C:/Users/`_USER\_NAME_ on Windows and `/home/`_USER\_NAME_ on Linux. It uses the same template as the global context, with the same possible variable names and values.

# Configuration variables #

A configuration file is composed of one or more lines in the
following format:

```
variable:value
```

Where _variable_ can be:

**flipPolicy**

  * DOUBLE\_FLIP\_POLICY - this should work for modern boards/drivers
  * SINGLE\_FLIP\_POLICY - use this for Intel 945 under Windows or other cheap boards
  * FBO\_FLIP\_POLICY - use this for modern boards/drivers where flip uses swap and not copy
  * ACCUM\_FLIP\_POLICY - use this for cheap boards where 'SINGLE' produces too much flickering
  * BACKUP\_FLIP\_POLICY - this is the default but isn't optimal regarding performance

**multisample**

  * True _(default)_
  * False

> Whether or not to try to obtain an OpenGL context supporting multisampling. This usually produces nicer results but is unsupported in older hardware. Even if this is set to false, however, pyprocessing will fallback to a non-multisampled config if it is not supported.

**coordInversionHack**

  * True _(default)_
  * False

> Whether or not to invert the y axis. This is required for strict conformity with Processing. Beyond altering the modelview matrix, this also implies that the drawing of some primitives such as arc or text are modified.

**halfPixelShiftHack**

  * True
  * False _(default)_

Since OpenGL actually addresses lines between pixels, in some cases shifting the drawing by half a pixel makes lines sharper.

**smoothFixHack**

  * True
  * False _(default)_

Try to get around the artifacts when drawing filled polygons in smooth mode.

# Example #

As example, this would be a valid contents for the globalconfig.txt file:

```
multisample:True
smoothFixHack:False
flipPolicy:FBO_FLIP_POLICY
```

# Setup Helper #

Pyprocessing also offers a simple setup application that helps you choose which flip policy is best suited for your hardware. It can be found on the default installation folder and is called FLIP\_SETUP.py. When run, it will display an animation using the current flip policy, allowing you to choose if the configuration is OK or if you want to change it. In the latter case, support for different policies are automatically checked and the policy value is changed. Lastly, the setup runs itself again, allowing the user to see if the new configuration is now working.