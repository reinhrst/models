This repo contains 3d models, written out as Blender python scripts. I find it much easier to create and write my models like this. For one, there can be proper version control on them. Secondly, I don't have to worry that at some point I did an operation that I didn't quite understand and from now on it influences everything I do.

I'm still looking for a good way to run things in a clean blender environment: http://blender.stackexchange.com/questions/18930/reset-blender-environment-on-each-script-run?noredirect=1#comment26931_18930

My current lines are one time:

```python
import sys; import importlib; sys.path.append("/Users/reinoud/Dropbox/work/models/berker-b1"); import shared; import single; import tap; import single_and_tap;
```

and then for each reload (after clearing the stage, first time manually, afterwards with cmd-Z:
```python
importlib.reload(tap); importlib.reload(shared); importlib.reload(single); importlib.reload(single_and_tap); single_and_tap.build(); bpy.ops.ed.undo_push()
```
