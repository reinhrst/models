This repo contains 3d models, written out as Blender python scripts. I find it much easier to create and write my models like this. For one, there can be proper version control on them. Secondly, I don't have to worry that at some point I did an operation that I didn't quite understand and from now on it influences everything I do.

To run the script in blender, what I use is open blender, select the scripting environment, and in the python console:
```python
filename="/path/to/file.py"
exec(compile(open(filename).read(), filename, "exec"))
```

Now I haven't found a good way yet to clear the scene. I would prefer every run of the script to start with the default screen, but as an alternative I just delete all objects in sight.
This fails though for hidden objects, so any subsequent load of the script (after editing it) is preceded by the `unhide()` function:

```python
unhide(); exec(compile(open(filename).read(), filename, "exec"))
```
