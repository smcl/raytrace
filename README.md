# raytrace

My implementation of [Raytracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html) but using Python instead of C++. I ended up also writing a simple NetPbm viewer that I started calling [feep](https://github.com/smcl/NetPbmViewer).

There are a number of things I wanted to to:

- a few places we inject parameters and rely on calling `something.update(newvalues)` to update it. maybe just return tuples instead as this is n-a-s-t-y
- tame the giant beast that is rt.py, it's quite big and could be split into a number of files I think
- don't just call the main "mptest.py"
- implement polygon primitive (and some helper functions to define squares, pyramids and prisms)
