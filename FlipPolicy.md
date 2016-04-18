## Double Buffering in OpenGL ##

OpenGL, the graphics library used in pyprocessing, supports what is called "double buffering". The idea is to allow applications to draw on a hidden buffer, called the _back buffer_, and only after the drawing is finished, it shown to the user by making it the _front buffer_, i.e., the buffer that is actually shown on the screen. This process is called _flipping_ the buffers.

In most cases where a modern graphics board is supported
by a recent driver, flipping works by copying the back to the front buffer. This is the best choice since further drawing may be done on the back buffer. Many applications
rely on this behavior since the screen is not completely redrawn from
scratch between one frame and the next.

Some drivers, however, do not implement flip by copying, but merely makes the
video controller address the other video memory buffer. This is what is called
flipping by _swapping_. It means that whenever the window needs to be redrawn it should not assume that previous contents is still there.

## Flipping in pyprocessing ##

[Processing](http://www.processing.org) assumes that the screen is stable, i.e., it should change only when the application explicitly draws on it. Thus, flipping by copying is OK, but flipping by swapping is NOT OK!

Pyprocessing just uses a regular [pyglet](http://www.pyglet.org) window, which is not concerned with maintaining a stable drawing surface. Since modern OpenGL implementations perform flipping by copying, this is not a problem. On those rare cases where flipping is done by swapping, pyprocessing offers alternative flip policies.

Currently, pyprocessing supports five flip policies controlled by five constants:

  1. `DOUBLE_FLIP_POLICY`: this should work for modern boards/drivers. If your application draws each frame from scratch, this will also work, even when flipping is done by swapping.
  1. `SINGLE_FLIP_POLICY`: means that no double buffering is to be used at all. This is usually a bad option since it tends to produce flickering between successive animation frames. For some boards, however, it works OK, especially if the drawing is created only once. For instance, if your pyprocessing application does not have a `draw()` function, but merely calls a few drawing functions in the main program, this should be OK.
  1. `FBO_FLIP_POLICY`: use this for modern boards/drivers where, nevertheless, flip uses swap and not copy. The idea here is that drawing actually takes place on a separate _frame buffer object (FBO)_. An FBO is an offscreen buffer which can be drawn to directly. When a flip operation is needed, the FBO is copied to the back buffer just before swapping.
  1. `ACCUM_FLIP_POLICY`: use this for cheap boards. It is horribly inefficient since it must copy buffers twice for each frame: (1) just before the flip when the contents of the back buffer are copied to the accumulation buffer, and (2) just after the flip when the accumulation buffer are restored to the back buffer.
  1. `BACKUP_FLIP_POLICY`: this is set as default because of compatibility. As with ACCUM\_FLIP\_POLICY, it is not efficient, since it makes a backup of the back buffer inside the main memory, making it necessary to move the buffer's contents twice between the GPU's and main memories for every flip.

To enforce a given flip policy in an application, call hint(constant) just before calling size(), where constant is one of the above constants. If you want to change the package's or a user's default policy, there's a guide covering that in the Preferences page.