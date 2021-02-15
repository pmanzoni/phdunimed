# PART 2: Building an image: basic steps

[![hackmd-github-sync-badge](https://hackmd.io/F192w34sRsW-1JfSXfOKUQ/badge)](https://hackmd.io/F192w34sRsW-1JfSXfOKUQ)


> https://training.play-with-docker.com/ops-s1-images/

First thing you may want to do is figure out how to create our own images. While there are over 700K images on Docker Store it is almost certain that none of them are exactly what you run in your data center today. Even something as common as a Windows OS image would get its own tweaks before you actually run it in production. 

We will start with the simplest form of image creation, in which we simply commit one of our container instances as an image. Then we will explore a much more powerful and useful method for creating images: the Dockerfile.

We will then see how to get the details of an image through the inspection and explore the filesystem to have a better understanding of what happens under the hood.

## Image creation from a container
Let’s start by running an interactive shell in a ubuntu container:

```
$ docker container run -ti ubuntu bash
```
As you know from before, you just grabbed the image called “ubuntu” from Docker Store and are now running the bash shell inside that container.

To customize things a little bit we will install a package called [figlet](http://www.figlet.org/) in this container. Your container should still be running so type the following commands at your ubuntu container command line:

```
apt-get update
apt-get install -y figlet
figlet "hello docker"
```
You should see the words “hello docker” printed out in large ascii characters on the screen. Go ahead and exit from this container

```
exit
```
Now let us pretend this new figlet application is quite useful and you want to share it with the rest of your team. You could tell them to do exactly what you did above and install figlet in to their own container, which is simple enough in this example. But if this was a real world application where you had just installed several packages and run through a number of configuration steps the process could get cumbersome and become quite error prone. Instead, it would be easier to create an image you can share with your team.

To start, we need to get the ID of this container using the ls command (do not forget the -a option as the non running container are not returned by the ls command).

```
$ docker container ls -a
```
Before we create our own image, we might want to inspect all the changes we made. Try typing the command 

```
$ docker container diff <container ID>
```

for the container you just created. You should see a list of all the files that were added to or changed in the container when you installed figlet. Docker keeps track of all of this information for us. This is part of the layer concept we will explore in a few minutes.

Now, to create an image we need to “commit” this container. Commit creates an image locally on the system running the Docker engine. Run the following command, using the container ID you retrieved, in order to commit the container and create an image out of it.

```
$ docker container commit CONTAINER_ID
```
That’s it - you have created your first image! Once it has been commited, we can see the newly created image in the list of available images.

```
$ docker image ls
```
You should see something like this:

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              a104f9ae9c37        46 seconds ago      160MB
ubuntu              latest              14f60031763d        4 days ago          120MB
```

Note that the image we pulled down in the first step (ubuntu) is listed here along with our own custom image. Except our custom image has no information in the REPOSITORY or TAG columns, which would make it tough to identify exactly what was in this container if we wanted to share amongst multiple team members.

Adding this information to an image is known as tagging an image. From the previous command, get the ID of the newly created image and tag it so it’s named ourfiglet:

```
$ docker image tag <IMAGE_ID> ourfiglet
$ docker image ls
```
Now we have the more friendly name “ourfiglet” that we can use to identify our image.

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ourfiglet           latest              a104f9ae9c37        5 minutes ago       160MB
ubuntu              latest              14f60031763d        4 days ago          120MB
```
Here is a graphical view of what we just completed: 

![](https://i.imgur.com/UGEg3cA.png)



Now we will run a container based on the newly created ourfiglet image:

```
$ docker container run ourfiglet figlet hello
```
As the figlet package is present in our ourfiglet image, the command returns the following output:

```
 _          _ _
| |__   ___| | | ___
| '_ \ / _ \ | |/ _ \
| | | |  __/ | | (_) |
|_| |_|\___|_|_|\___/

```
This example shows that we can create a container, add all the libraries and binaries in it and then commit it in order to create an image. We can then use that image just as we would for images pulled down from the Docker Store. We still have a slight issue in that our image is only stored locally. To share the image we would want to push the image to a registry somewhere. We'll see how to do this later...

This approach of manually installing software in a container and then committing it to a custom image is just one way to create an image. It works fine and is quite common. However, there is a more powerful way to create images. In the following exercise we will see how images are created using a Dockerfile, which is a text file that contains all the instructions to build an image.

## Image creation using a Dockerfile

Instead of creating a static binary image, we can use a file called a Dockerfile to create an image. The final result is essentially the same, but with a Dockerfile we are supplying the instructions for building the image, rather than just the raw binary files. This is useful because it becomes much easier to manage changes, especially as your images get bigger and more complex.

Dockerfiles are powerful because they allow us to manage how an image is built, rather than just managing binaries. In practice, Dockerfiles can be managed the same way you might manage source code: they are simply text files so almost any version control system can be used to manage Dockerfiles over time.

We will use a simple example in this section and build a “hello world” application in Node.js. Do not be concerned if you are not familiar with Node.js: Docker (and this exercise) does not require you to know all these details.

We will start by creating a file in which we retrieve the hostname and display it. 

Type the following content into a file named `index.js`:

```
var os = require("os");
var hostname = os.hostname();
console.log("hello from " + hostname);
```
The file we just created is the javascript code for our server. As you can probably guess, Node.js will simply print out a “hello” message. We will: 
* Docker-ize this application by creating a Dockerfile; we will use alpine as the base OS image, 
* add a Node.js runtime and then 
* copy our source code in to the container. 
* We will also specify the default command to be run upon container creation.

Create a file named Dockerfile and copy the following content into it. Again, help creating this file with Linux editors is here 3.

```
FROM alpine
RUN apk update && apk add nodejs
COPY . /app
WORKDIR /app
CMD ["node","index.js"]
```
Let’s build our first image out of this Dockerfile and name it hello:v0.1:

```
$ docker image build -t hello:v0.1 .
```
This is what you just completed: 

![](https://i.imgur.com/a0IzXbZ.png)


We then start a container to check that our applications runs correctly:

```
$ docker container run hello:v0.1
```
You should then have an output similar to the following one (the ID will be different though).

```
hello from 92d79b6de29f
```
What just happened? We created two files: our application code (index.js) is a simple bit of javascript code that prints out a message. And the Dockerfile is the instructions for Docker engine to create our custom container. This Dockerfile does the following:

1. Specifies a base image to pull FROM - the alpine image we used in earlier labs.
2. Then it RUNs two commands (apk update and apk add) inside that container which installs the Node.js server.
3. Then we told it to COPY files from our working directory in to the container. The only file we have right now is our index.js.
4. Next we specify the WORKDIR - the directory the container should use when it starts up
5. And finally, we gave our container a command (CMD) to run when the container starts.

Recall that in previous labs we put commands like echo "hello world" on the command line. With a Dockerfile we can specify precise commands to run for everyone who uses this container. Other users do not have to build the container themselves once you push your container up to a repository (which we will cover later) or even know what commands are used. The Dockerfile allows us to specify how to build a container so that we can repeat those steps precisely everytime and we can specify what the container should do when it runs. There are actually multiple methods for specifying the commands and accepting parameters a container will use, but for now it is enough to know that you have the tools to create some pretty powerful containers.

## Image layers

There is something else interesting about the images we build with Docker. When running they appear to be a single OS and application. But the images themselves are actually built in layers. If you scroll back and look at the output from your docker image build command you will notice that there were 5 steps and each step had several tasks. You should see several “fetch” and “pull” tasks where Docker is grabbing various bits from Docker Store or other places. These bits were used to create one or more container layers. Layers are an important concept. To explore this, we will go through another set of exercises.

First, check out the image you created earlier by using the history command (remember to use the docker image ls command from earlier exercises to find your image IDs):

```
$ docker image history <image ID>
```
What you see is the list of intermediate container images that were built along the way to creating your final Node.js app image. Some of these intermediate images will become layers in your final container image. In the history command output, the original Alpine layers are at the bottom of the list and then each customization we added in our Dockerfile is its own step in the output. This is a powerful concept because it means that if we need to make a change to our application, it may only affect a single layer! To see this, we will modify our app a bit and create a new image.

Type the following in to your console window:

```echo "console.log(\"this is v0.2\");" >> index.js```

This will add a new line to the bottom of your index.js file from earlier so your application will output one additional line of text. Now we will build a new image using our updated code. We will also tag our new image to mark it as a new version so that anybody consuming our images later can identify the correct version to use:

```
$ docker image build -t hello:v0.2 .
```
You should see output similar to this:

```
Sending build context to Docker daemon  86.15MB
Step 1/5 : FROM alpine
 ---> 7328f6f8b418
Step 2/5 : RUN apk update && apk add nodejs
 ---> Using cache
 ---> 2707762fca63
Step 3/5 : COPY . /app
 ---> 07b2e2127db4
Removing intermediate container 84eb9c31320d
Step 4/5 : WORKDIR /app
 ---> 6630eb76312c
Removing intermediate container ee6c9e7a5337
Step 5/5 : CMD node index.js
 ---> Running in e079fb6000a3
 ---> e536b9dadd2f
Removing intermediate container e079fb6000a3
Successfully built e536b9dadd2f
Successfully tagged hello:v0.2
```
Notice something interesting in the build steps this time. In the output it goes through the same five steps, but notice that in some steps it says Using cache.

![](https://i.imgur.com/rCjMl4b.png)

Docker recognized that we had already built some of these layers in our earlier image builds and since nothing had changed in those layers it could simply use a cached version of the layer, rather than pulling down code a second time and running those steps. Docker’s layer management is very useful to IT teams when patching systems, updating or upgrading to the latest version of code, or making configuration changes to applications. Docker is intelligent enough to build the container in the most efficient way possible, as opposed to repeatedly building an image from the ground up each and every time.

## Image Inspection
Now let us reverse our thinking a bit. What if we get a container from Docker Store or another registry and want to know a bit about what is inside the container we are consuming? Docker has an inspect command for images and it returns details on the container image, the commands it runs, the OS and more.

The alpine image should already be present locally from the exercises above (use docker image ls to confirm), if it’s not, run the following command to pull it down:

```
$ docker image pull alpine
```
Once we are sure it is there let’s inspect it.

```
$ docker image inspect alpine
```
There is a lot of information in there:

* the layers the image is composed of
* the driver used to store the layers
* the architecture / OS it has been created for
* metadata of the image
* …


We will not go into all the details here but we can use some filters to just inspect particular details about the image. You may have noticed that the image information is in JSON format. We can take advantage of that to use the inspect command with some filtering info to just get specific data from the image.

Let’s get the list of layers:

```$ docker image inspect --format "{{ json .RootFS.Layers }}" alpine```

Alpine is just a small base OS image so there’s just one layer:

```
["sha256:60ab55d3379d47c1ba6b6225d59d10e1f52096ee9d5c816e42c635ccc57a5a2b"]
```
Now let’s look at our custom Hello image. You will need the image ID (use docker image ls if you need to look it up):

```docker image inspect --format "{{ json .RootFS.Layers }}" <image ID```
Our Hello image is a bit more interesting (your sha256 hashes will vary):

`["sha256:5bef08742407efd622d243692b79ba0055383bbce12900324f75e56f589aedb0","sha256:5ac283aaea742f843c869d28bbeaf5000c08685b5f7ba01431094a207b8a1df9","sha256:2ecb254be0603a2c76880be45a5c2b028f6208714aec770d49c9eff4cbc3cf25"]`
We have three layers in our application. Recall that we had the base Alpine image (the FROM command in our Dockerfile), then we had a RUN command to install some packages, then we had a COPY command to add in our javascript code. Those are our layers! If you look closely, you can even see that both alpine and hello are using the same base layer, which we know because they have the same sha256 hash.

## Final notes
The tools and commands we explored in this lab are just the beginning. Docker Enterprise Edition includes private Trusted Registries with Security Scanning and Image Signing capabilities so you can further inspect and authenticate your images. In addition, there are policy controls to specify which users have access to various images, who can push and pull images, and much more.

Another important note about layers: each layer is immutable. As an image is created and successive layers are added, the new layers keep track of the changes from the layer below. When you start the container running there is an additional layer used to keep track of any changes that occur as the application runs (like the “hello.txt” file we created in the earlier exercises). This design principle is important for both security and data management. If someone mistakenly or maliciously changes something in a running container, you can very easily revert back to its original state because the base layers cannot be changed. Or you can simply start a new container instance which will start fresh from your pristine image. And applications that create and store data (databases, for example) can store their data in a special kind of Docker object called a volume, so that data can persist and be shared with other containers. 
