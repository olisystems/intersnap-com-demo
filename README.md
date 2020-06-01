# The Joy of Building Snaps for Python Applications

<!-- MDTOC maxdepth:6 firsth1:0 numbering:1 flatten:0 bullets:0 updateOnSave:1 -->

1. [Prerequisites](#prerequisites)   
&emsp;1.1. [Install Snap on Ubuntu](#install-snap-on-ubuntu)   
&emsp;1.2. [Install Snapcraft](#install-snapcraft)   
2. [Process of Building a Snap](#process-of-building-a-snap)   
&emsp;2.1. [List Snap's Requirements](#list-snaps-requirements)   
&emsp;2.2. [Initialising snap environment](#initialising-snap-environment)   
&emsp;2.3. [Add Interface to Snap](#add-interface-to-snap)   
&emsp;&emsp;2.3.1. [Creating .yaml file for Reader Snap](#creating-yaml-file-for-reader-snap)   
&emsp;2.4. [Build Writer Snap](#build-writer-snap)   
&emsp;&emsp;2.4.1. [Create Reader Snap](#create-reader-snap)   
&emsp;2.5. [Publish Snap](#publish-snap)   
3. [References](#references)   
4. [Contributing](#contributing)   
5. [License](#license)   

<!-- /MDTOC -->
While building applications in Python, we have to deal with dependency management that is not easy especially when it comes to package and ship your app. A snap bundles an application and all its dependencies to work across a range of Linux distributions. Snaps can be found and installed from the [snap store](https://snapcraft.io/store).

In this tutorial, We will create two snaps to persist the user config data and then share this data with a _consumer_ snap. The applications are developed in Python.

- `writer snap` that will persist user config data to `$SNAP_DATA`
- `reader snap` that will read the config data file created by the `writer` snap

This tutorial has been written using Ubuntu 20.04 LTS and it should work without modifications for other Ubuntu releases (18.04 LTS, 19.10 LTS). The tutorial aims to give an overview of building snaps and their advanced usage. We will use a command-line tool, called Snapcraft, for building snap which reads the snap metadata from a declarative file and runs the build.

## Prerequisites

We need to install `snap` and `snapcraft` before we start building snaps.

### Install Snap on Ubuntu

For Ubuntu 16.04 LTS (Xenial Xerus) and later, snap is pre-installed and ready to go. However, use the following commands to install the snap if it is not already installed:

```
sudo apt update
sudo apt install snapd
```

Type the following command to make sure that snap is correctly installed:

```
snap --version
```

You should see an output similar to this:

```
snap    2.44.3+20.04
snapd   2.44.3+20.04
series  16
ubuntu  20.04
kernel  5.4.0-33-generic
```

### Install Snapcraft

Next, we need to install snapcraft command-line tool for building snaps by running the following command in the terminal:

```
sudo snap install --classic snapcraft
```

## Process of Building a Snap

The process of building a snap can be divided into four steps:

1. List snap's requirements
2. Initializing snap environment
3. Add interfaces to snap
4. Create snap
5. Publish and share

### List Snap's Requirements

Usually, the requirements of a snap are the same as the requirements of the application itself. The [writer](https://github.com/olisystems/intersnap-com-demo/tree/master/writer-snap) app has the functionality to take user input using a Python package called [click](https://click.palletsprojects.com/en/7.x/) and then persist this input into a `toml` file.

The requirements for the [reader](https://github.com/olisystems/intersnap-com-demo/tree/master/reader-snap) snap are pretty much simple, it has to read the configs saved by `writer` app and print them to console.

As both of our apps are fairly simple, I'll skip the app development process for now. Once we have developed our apps, next is to initialize the snap environment.

### Initialising snap environment

Initializing snap environment involves creating a `snapcraft.yaml` file that provides metadata for the snap. Initialize the snap environment by typing the following command in the root `writer-snap`:

```
snapcraft init
```

The result of the above command is a `snapcraft.yaml` template with [mandatory snap's metadata](https://snapcraft.io/docs/adding-global-metadata) inside the `snap` sub-directory.

Let's add some necessary [parts](https://snapcraft.io/docs/adding-parts) to describe our application.

1. The first section in the `parts` describes the source and plugin definition.

```
[...]
parts:
  writer-snap:
    source: .
    plugin: python
    requirements: ['requirements.txt']
```

Note: `[...]` represents the rest part of the code.

In the above code snippet, `writer-snap` is the arbitrary part name. Next is the source for which has specified the current repository. Other options for the source could be git or a tarball. We are using Python plugin that reads app requirements from the `requirements.txt` file located in the root of the project.

2. In our app, we want to create a `config.toml` file if it does not exist already and then write configs to this file. To do that, we will create the following [wrapper script](https://github.com/olisystems/intersnap-com-demo/blob/master/writer-snap/writer.sh) in the root directory of our project:

```sh
#! /bin/sh

[ -e "$SNAP_DATA/config.toml" ] || touch $SNAP_DATA/config.toml

exec "$@"
```

Now we need to make this script executable and then ship it in `bin/`. Run the following command in the root of the project:

```
sudo chmod +x writer.sh
```

3. To ship executable script to the `bin/`, we will add the following part in `parts`:

```
[...]
  launcher:
    plugin: nil
    source: .
    override-build: |
      mkdir -p $SNAPCRAFT_PART_INSTALL/bin
      cp -av writer.sh $SNAPCRAFT_PART_INSTALL/bin/
```

The above part will create a directory `$SNAPCRAFT_PART_INSTALL/bin` and copy the `writer.sh` script over there.

4. Finally, we need to change the [command](https://snapcraft.io/docs/defining-a-command) entry in the `apps` section as follows:

```
[...]
apps:
  writer-snap:
    command: writer.sh writer-snap
```

### Add Interface to Snap

To share data between the snaps, we are going to use the [content interface](https://snapcraft.io/docs/content-interface). The content interface makes it possible to share data from a producer snap to one or more consumer snaps. The sharing of data happens at the filesystem level including executables, libraries, data files, and sockets also.

Add the following content slot to the `snapcraft.yaml` file:

```
[...]
slots:
  shared-files:
    interface: content
    content: shared-files
    read:
      - $SNAP_DATA
```

The `content` attribute describes the content and this attribute must be the same on both sides to establish the connection. The `read` attribute declares which part should be read by the `reader` snap.

The complete snapcraft.yaml file for the `writer` snap can be found [here](https://github.com/olisystems/intersnap-com-demo/blob/master/writer-snap/snap/snapcraft.yaml).

#### Creating .yaml file for Reader Snap

Creating the snapcraft.yaml file for the [reader](https://github.com/olisystems/intersnap-com-demo/tree/master/reader-snap) snap is relatively simple as it will just read the configs. Repeat the aforementioned steps, except `launcher` part, for `reader` snap as well and add the content plug to the reader's [snapcraft.yaml](https://github.com/olisystems/intersnap-com-demo/blob/master/reader-snap/snap/snapcraft.yaml) file as follows:

```
plugs:
  shared-files:
    interface: content
    content: shared-files
    target: $SNAP_DATA
```

### Build Writer Snap

Once we are done with the `yaml` file, it is time to create the snap. We will start creating the snap by running the following command with debug mode in the root of `writer-snap`:

```
snapcraft --debug
```

The output of the above command will look like this:

```
[...]
Building writer-snap-data
Staging launcher
Staging writer-snap
Staging writer-snap-data
Priming launcher
Priming writer-snap
Priming writer-snap-data
Snapping 'writer-snap' |
Snapped writer-snap_0.1dev_amd64.snap
```

Congratulations! we have just created our first snap.

Note: When you run the command for the first time, you may prompt to install the multipass.

The newly created snap can be installed with the following command in the `dev` mode:

```
sudo snap install writer-snap_0.1dev_amd64.snap --devmode
```

The output will be like:

```
writer-snap 0.1dev installed
```

Finally, run the snap with the following command:

```
sudo writer-snap
```

Note: You can just hit enter to save the default configs without typing anything.

Additionally, you can run the following command to see info about the installed snap:

```
snap list writer-snap
```

The output should look like:

```
Name         Version  Rev  Tracking  Publisher  Notes
writer-snap  0.1dev   x1   -         -          devmode
```

You can check the contents of the config file with the following command:

```
sudo nano /var/snap/writer-snap/x1/config.toml
```

#### Create Reader Snap

To create the `reader` snap, repeat the above-described process.

Once the `reader` snap is created and installed, we need to make a connection between the `writer` and the `reader` snap.

To make a connection, use the following syntax:

```
snap connect <snap>:<plug interface> <snap>:<slot interface>
```

In our case the command will be:

```
snap connect reader-snap:shared-files writer-snap:shared-files
```

After establishing the connection, run the following command:

```
reader-snap
```

The output should look like:

```js
dict_items([
  ("title", "Building Python Snaps"),
  ("mqtt_connection",
  {
    mqtt_broker_ip: "unbelievable-politician.cloudmqtt.com",
    mqtt_broker_port: "8883",
    ssl_cert_path: "ca-certificates.crt",
    mqtt_username: "username",
  }),
]);
```

To disconnect an interface, use snap disconnect:

```
snap disconnect <snap>:<plug interface> <snap>:<slot interface>
```

### Publish Snap

Publishing the application to the snap store can be done in three steps:

1. Create a developer account on [the dashboard](https://login.ubuntu.com/v4apP4ET6CxsCIHS/+decide)
2. Register application’s name on [dashboard.snapcraft.io](https://dashboard.snapcraft.io/register-snap/)
3. Upload your application

## References

https://snapcraft.io/docs/python-apps

https://ubuntu.com/tutorials/create-your-first-snap#1-overview

https://forum.snapcraft.io/t/how-to-persist-user-config-data-to-snap-user-data/15464

https://www.youtube.com/watch?v=BEp_l2oUcD8&feature=emb_logo

## Contributing

Pull requests are welcome.

1. Fork the repository.
2. Create your new feature branch: `git checkout -b new-feature-branch`
3. Stage your changes: `git add .`
4. Commit the changes: `git commit -m "add commit message"`
5. `push` to the branch: `git push origin new-feature-branch`
6. Submit a `pull request`.


## License

This project is licensed under the [MIT](./LICENSE) License.
