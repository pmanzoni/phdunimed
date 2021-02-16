[![hackmd-github-sync-badge](https://hackmd.io/oNBMMGCPRmyrjxM6xmXMmw/badge)](https://hackmd.io/oNBMMGCPRmyrjxM6xmXMmw)


# Docker: the basics
> based on     
> * https://training.play-with-docker.com/dev-stage1/
> * https://training.play-with-docker.com/ops-s1-hello/


:::info
Option 1:
You can download and install Docker on multiple platforms. Refer to the following link: 
https://docs.docker.com/get-docker/
and choose the best installation path for you.

Option 2: 
You can use a virtual machine that you can [download here](https://www.dropbox.com/s/frur6hfwanc9fwl/ubudocker.ova?dl=0)
You have to use  VirtualBox  with the option: "Files / Import virtualized service".
The VM has user "**docker**" with password "**docker**"

Option 3:
You can execute it online: 
https://labs.play-with-docker.com/

:::






## Playing with containers

There are different ways to use containers. These include:

* To run a **single task**: This could be a shell script or a custom app.
* **Interactively**: This connects you to the container similar to the way you SSH into a remote server.
* In the **background**: For long-running services like websites and databases.



## Run a single task "Hello World"

```
$ docker container run hello-world
```

![](https://i.imgur.com/113RKn6.png)

----

## Docker Hub (https://hub.docker.com/)

![](https://i.imgur.com/elVmVtM.png)

----

### [`https://hub.docker.com/_/hello-world`](https://hub.docker.com/_/hello-world)

![](https://i.imgur.com/ntTx3DW.png)

----

### [`https://github.com/docker-library/hello-world`](https://github.com/docker-library/hello-world)

![](https://i.imgur.com/6raUc92.png)

----

![](https://i.imgur.com/uIEHAxT.png)

----

![](https://i.imgur.com/H04ybMY.png)

----

![](https://i.imgur.com/K70YOpe.png)

---


For simplicity, you can think of an image as a git repository, that is images can be [committed](https://docs.docker.com/engine/reference/commandline/commit/) with changes and have multiple versions. 

For example you could pull a specific version of `ubuntu` image as follows:

```bash
$ docker pull ubuntu:12.04
```

If you do not specify the version number of the image the Docker client will default to a version named `latest`.

So for example, the `docker pull` command given below will pull an image named `ubuntu:latest`:

```bash
$ docker pull ubuntu
```

To get a new Docker image you can either get it from a registry (such as the Docker Store) or create your own. There are hundreds of thousands of images available on [Docker Hub](https://store.docker.com). You can also search for images directly from the command line using `docker search`.




## Run an interactive Ubuntu container

The following command runs an ubuntu container, attaches interactively ('`-i`') to your local command-line session ('`-t`'), and runs /bin/bash.

    $ docker run -i -t ubuntu /bin/bash

---

1. If you do not have the ubuntu image locally, Docker pulls it from your configured registry.
1. Docker creates a new container.
1. Docker allocates a read-write filesystem to the container, as its final layer. 
1. Docker creates a network interface to connect the container to the default network. By default, containers can connect to external networks using the host machine’s network connection.
1. Docker starts the container and executes `/bin/bash`. 
1. When you type `exit` to terminate the `/bin/bash` command, the container stops but is not removed. You can start it again or remove it.

---

You can check the images you downloaded using:
```
$ docker image ls
```
and the containers using:
```
$ docker container ls -a
```

:::info
**By the way...**
In the rest of this seminar, we are going to run an ==Alpine Linux== container. Alpine (https://www.alpinelinux.org/) is a lightweight Linux distribution so it is quick to pull down and run, making it a popular starting point for many other images.
:::

```
$ docker image pull alpine

$ docker image ls
```
Some examples:
```
$ docker container run alpine echo "hello from alpine"

$ docker container run alpine ls -l
```
![](https://i.imgur.com/1iQnej7.png)

More examples:
```
$ docker container run alpine /bin/sh

$ docker container run -it alpine /bin/sh
```

Which is the difference between these two examples?

<!--
E.g., try:
`/ # ip a `
-->

---

## Docker container instances

```
$ docker container ls

$ docker container ls -a
```

![](https://i.imgur.com/1XrlIr6.png)

---

## Container Isolation

This is a critical security concept in the world of Docker containers! **Even though each docker container run command used the same alpine image, each execution was a separate, isolated container.** Each container has a separate filesystem and runs in a different namespace; by default a container has no way of interacting with other containers, even those from the same image. 

So, let's see:

``` 
$ docker container run -it alpine /bin/ash
/ # echo "hello world" > hello.txt
/ # ls
```

we get to something like this:
![](https://i.imgur.com/9OR5wVe.png)

To show all Docker containers (both running and stopped) we use `$ docker ps -a`. We will get something like this:

```
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
ed8cfb69af14        alpine              "/bin/ash"               3 minutes ago       Exited (0) 10 seconds ago                       optimistic_chatterjee
e700ae985bc0        alpine              "/bin/sh"                5 minutes ago       Exited (0) 5 minutes ago                        zen_goldstine
...
```
Now if we do:

``` 
$ docker container start e700ae985bc0
$ docker exec e700ae985bc0 ls -l
```

We will see that in that container there is not the file "hello.txt"!

## Handling containers

To summarize a little.

To show which Docker containers are running:
```
$ docker ps
``` 
To show all Docker containers (both running and stopped):
```
$ docker ps -a
```
If you don't see your container in the output of `docker ps -a` command, than you have to run an image:
```
$ docker run ...
```

If a container appears in `docker ps -a`  but not in `docker ps`, the container has stopped, you have to restart it:

```
$ docker container start <container ID>
```

If the Docker container is already running (i.e., listed in `docker ps`), you can reconnect to the container in each terminal:

```
$ docker exec -it <container ID> sh
```

### Detached containers

Starts an Alpine container using the  `-dit` flags running `ash`. The container will start **detached** (in the background), interactive (with the ability to type into it), and with a TTY (so you can see the input and output). Since you are starting it detached, you won’t be connected to the container right away.

```
$ docker run -dit --name alpine1 alpine ash
```

Use the docker `attach` command to connect to this container:

```bash 
$ docker attach alpine1
/ #
```

Detach from alpine1 without stopping it by using the detach sequence, `CTRL + p CTRL + q` (*hold down CTRL and type p followed by q*). 

If you want to keep the container running after the end of the session, you need to daemonize it:

```
docker run --name daemon -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done" 
```

Let’s check the logs and see what the daemon container is doing right now:

```
docker logs -f daemon  
```
Console output:

```
...
hello world  
hello world  
hello world  
```

docker logs fetch the logs of a container, the `-f` flag to follow the log output (works actually like tail -f).



### Finally:
```
$ docker container stop <node name> (or <container id>)

$ docker container rm <node name> (or <container id>)

```

