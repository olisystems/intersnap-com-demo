
# The Inter-Snap Communication

This is a demo project to show inter-snap communicaiton using the content interface.

## The Content Interface

The content interface makes it possible to share data from a _producer_ snap to one or more _consumer_ snaps. The sharing of data happens at the filesystem level including executables, libraries, data files and sockets also.

Some important points while using the content interface are:

* Read, write and target should start with either `$SNAP`, `$SNAP_DATA` or `$SNAP_COMMON` to refer to the designated directory.

* The content identifier specified by the consuming snap (plug) must match the content attribute of the producer snap (slot).

* At a very basic level, the content interface enables one directory, file or socket to appear in a place where another snap can access it.

To make a connection, use the following syntax:

```
$ snap connect <snap>:<plug interface> <snap>:<slot interface>
```

To disconnect an interface, use snap disconnect:

```
$ snap disconnect <snap>:<plug interface> <snap>:<slot interface>
```

### References

https://snapcraft.io/docs/content-interface