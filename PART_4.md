[![hackmd-github-sync-badge](https://hackmd.io/oNBMMGCPRmyrjxM6xmXMmw/badge)](https://hackmd.io/oNBMMGCPRmyrjxM6xmXMmw)
> To clean Docker: docker system prune -a


# PART 4:  Building an image: an example with Flask

>**Note:** This lab is based on [Docker Tutorials and Labs](https://github.com/docker/labs/blob/master/beginner/chapters/webapps.md#23-create-your-first-image).
---


## Docker Images
In this section we will build our own image, use that image to run an application locally, and finally, push some of our own images to the 
[![](https://i.imgur.com/e1O1LbO.png)](https://hub.docker.com/) 
:::info
The docker hub is also referred to as Docker Store or Docker Cloud.
:::



---


For simplicity, you can think of an image as a git repository, that is images can be [committed](https://docs.docker.com/engine/reference/commandline/commit/) with changes and have multiple versions. 

For example you could pull a specific version of `ubuntu` image as follows:

```bash
$ docker pull ubuntu:12.04
```

---


If you do not specify the version number of the image the Docker client will default to a version named `latest`.

So for example, the `docker pull` command given below will pull an image named `ubuntu:latest`:

```bash
$ docker pull ubuntu
```

---


To get a new Docker image you can either get it from a registry (such as the Docker Store) or create your own. There are hundreds of thousands of images available on [Docker Hub](https://store.docker.com). You can also search for images directly from the command line using `docker search`.

---


An important distinction with regard to images is between _base images_ and _child images_.

- **Base images** are images that have no parent images, usually images with an OS like ubuntu, alpine or debian.

- **Child images** are images that are built on base images and add additional functionality.

---


Another key concept is the idea of _official images_ and _user images_. (Both of which can be base images or child images.)

- **Official images** are Docker sanctioned images. Docker, Inc. sponsors a dedicated team that is responsible for reviewing and publishing all Official Repositories content. This team works in collaboration with upstream software maintainers, security experts, and the broader Docker community. These are not prefixed by an organization or user name. Images like `python`, `node`, `alpine` and `nginx` are official (base) images. 

:::info
To find out more about them, check out the [Official Images Documentation](https://docs.docker.com/docker-hub/official_repos/).
:::

- **User images** are images created and shared by users like you. They build on base images and add additional functionality. Typically these are formatted as `user/image-name`. The `user` value in the image name is your Docker Store user or organization name.

---
___


## Creating our first image
>**Note:** The code of this section is in [this repository](https://www.dropbox.com/sh/e6zxf2t76rvk7e7/AAC7voT8yMAZNkLPpd1iaF34a?dl=0). 



The goal of the next steps is to create a Docker image which will run a [Flask](http://flask.pocoo.org) app.

We'll do this by first pulling together the components for a _random pizza picture generator_ built with Python Flask, then _dockerizing_ it by writing a _Dockerfile_. Finally, we'll build the image, and then run it.

### Create a Python Flask app that displays random pizzas pix

For the purposes of this class, we use a little Python Flask app that displays a random pizza `.gif` every time it is loaded... :smiley:

We have to create the following files:
- app.py
- templates/index.html
- Dockerfile

---

#### app.py


```python
from flask import Flask, render_template
import random

app = Flask(__name__)

# Breakfast Pizzas That Want To Wake Up Next To You
# https://www.buzzfeed.com/rachelysanders/good-morning-pizza
images = [
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/13/enhanced/webdr10/enhanced-buzz-12910-1406051649-8.jpg",
...
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/14/enhanced/webdr02/enhanced-buzz-1275-1406053174-20.jpg"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    # 'flask run --host=0.0.0.0' tells your operating system to listen on all public IPs.
    app.run(host="0.0.0.0")
```

---


#### templates/index.html

```htmlmixed=
<html>
  <head>
    <style type="text/css">
      body {
        background: black;
        color: white;
      }
      div.container {
        max-width: 90%;
        margin: 100px auto;
        border: 20px solid white;
        padding: 10px;
        text-align: center;
      }
      h4 {
        text-transform: uppercase;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h4>Breakfast Pizzas of the day</h4>
      <img src="{{url}}" />
      <p><small>Courtesy: <a href="https://www.buzzfeed.com/rachelysanders/good-morning-pizza">Buzzfeed</a></small></p>
    </div>
  </body>
</html>
```

---


### the "Dockerfile"

We want to create a Docker image with this web app. As mentioned above, all user images are based on a _base image_. Since our application is written in Python, we will build our own Python image based on [Alpine](https://store.docker.com/images/alpine). 

To do this we need a **Dockerfile**.
A [Dockerfile](https://docs.docker.com/engine/reference/builder/) is a text file that contains a list of commands that the Docker daemon calls while creating an image. The Dockerfile contains all the information that Docker needs to know to run the app:
* a base Docker image to run from, 
* location of your project code, 
* any dependencies it has, 
* and what commands to run at start-up. 

It is a simple way to automate the image creation process. The best part is that the commands you write in a Dockerfile are *almost* identical to their equivalent Linux commands. This means you don't really have to learn new syntax to create your own Dockerfiles. So..

---


1. Create a file called **Dockerfile**, and  indicate the base image, using the `FROM` keyword:

```
FROM alpine:3.5
```

---


2. The next step usually is to write the commands of copying the files and installing the dependencies. But first we will install the Python `pip` package to the alpine linux distribution. This will not just install the pip package but any other dependencies too, which includes the python interpreter. Add the following [RUN](https://docs.docker.com/engine/reference/builder/#run) command next:

```
RUN apk add --update py2-pip
```

---


3. Install the Flask Application.

```
RUN pip install -U Flask
```
---

4. Copy the files you have created earlier into our image by using [COPY](https://docs.docker.com/engine/reference/builder/#copy)  command.

```
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/
```

---


5. Specify the port number which needs to be exposed. Since our flask app is running on `5000` that's what we'll expose.

```
EXPOSE 5000
```

---


6. The last step is the command for running the application which is simply: `python ./app.py`.
Use the [CMD](https://docs.docker.com/engine/reference/builder/#cmd) command to do that:

```
CMD ["python", "/usr/src/app/app.py"]
```

The primary purpose of `CMD` is to tell the container which command it should run by default when it is started.

---


7. The `Dockerfile` is now ready. This is how it looks:

```bash=
# our base image
FROM alpine:3.5

# Install python and pip
RUN apk add --update py2-pip

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python app
RUN pip install -U Flask

# copy files required for the app to run
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "/usr/src/app/app.py"]
```

---


### Build the image

Now that you have your `Dockerfile`, you can build your image. The `docker build` command does the heavy-lifting of creating a docker image from a `Dockerfile`.

When you run the `docker build` command given below, make sure to replace `<YOUR_USERNAME>` with your username. This username should be the same one you created when registering on [Docker Hub](https://cloud.docker.com). 

---


The `docker build` command is quite simple - it takes an optional tag name with the `-t` flag, and the location of the directory containing the `Dockerfile` - the `.` indicates the current directory:

```bash
$ docker build -t <YOUR_USERNAME>/myfirstapp .
```
the generated output is something similar to:
```bash
Sending build context to Docker daemon 9.728 kB
Step 1 : FROM alpine:latest
 ---> 0d81fc72e790
Step 2 : RUN apk add --update py-pip
 ---> Running in 8abd4091b5f5
fetch http://dl-4.alpinelinux.org/alpine/v3.3/main/x86_64/APKINDEX.tar.gz
fetch http://dl-4.alpinelinux.org/alpine/v3.3/community/x86_64/APKINDEX.tar.gz
(1/12) Installing libbz2 (1.0.6-r4)
(2/12) Installing expat (2.1.0-r2)
(3/12) Installing libffi (3.2.1-r2)
(4/12) Installing gdbm (1.11-r1)
(5/12) Installing ncurses-terminfo-base (6.0-r6)
(6/12) Installing ncurses-terminfo (6.0-r6)
(7/12) Installing ncurses-libs (6.0-r6)
(8/12) Installing readline (6.3.008-r4)
(9/12) Installing sqlite-libs (3.9.2-r0)
(10/12) Installing python (2.7.11-r3)
(11/12) Installing py-setuptools (18.8-r0)
(12/12) Installing py-pip (7.1.2-r0)
Executing busybox-1.24.1-r7.trigger
OK: 59 MiB in 23 packages
 ---> 976a232ac4ad
Removing intermediate container 8abd4091b5f5
Step 3 : COPY requirements.txt /usr/src/app/
 ---> 65b4be05340c
Removing intermediate container 29ef53b58e0f
Step 4 : RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
 ---> Running in a1f26ded28e7
Collecting Flask==0.10.1 (from -r /usr/src/app/requirements.txt (line 1))
  Downloading Flask-0.10.1.tar.gz (544kB)
Collecting Werkzeug>=0.7 (from Flask==0.10.1->-r /usr/src/app/requirements.txt (line 1))
  Downloading Werkzeug-0.11.4-py2.py3-none-any.whl (305kB)
Collecting Jinja2>=2.4 (from Flask==0.10.1->-r /usr/src/app/requirements.txt (line 1))
  Downloading Jinja2-2.8-py2.py3-none-any.whl (263kB)
Collecting itsdangerous>=0.21 (from Flask==0.10.1->-r /usr/src/app/requirements.txt (line 1))
  Downloading itsdangerous-0.24.tar.gz (46kB)
Collecting MarkupSafe (from Jinja2>=2.4->Flask==0.10.1->-r /usr/src/app/requirements.txt (line 1))
  Downloading MarkupSafe-0.23.tar.gz
Installing collected packages: Werkzeug, MarkupSafe, Jinja2, itsdangerous, Flask
  Running setup.py install for MarkupSafe
  Running setup.py install for itsdangerous
  Running setup.py install for Flask
Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.4 itsdangerous-0.24
You are using pip version 7.1.2, however version 8.1.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
 ---> 8de73b0730c2
Removing intermediate container a1f26ded28e7
Step 5 : COPY app.py /usr/src/app/
 ---> 6a3436fca83e
Removing intermediate container d51b81a8b698
Step 6 : COPY templates/index.html /usr/src/app/templates/
 ---> 8098386bee99
Removing intermediate container b783d7646f83
Step 7 : EXPOSE 5000
 ---> Running in 31401b7dea40
 ---> 5e9988d87da7
Removing intermediate container 31401b7dea40
Step 8 : CMD python /usr/src/app/app.py
 ---> Running in 78e324d26576
 ---> 2f7357a0805d
Removing intermediate container 78e324d26576
Successfully built 2f7357a0805d
```

---

If everything went well, your image should be ready! Run `$ docker images` and see if your image (`<YOUR_USERNAME>/myfirstapp`) shows.

---


### Run your image
The next step in this section is to run the image and see if it actually works.

```bash
$ docker run -p 8888:5000 --name myfirstapp YOUR_USERNAME/myfirstapp
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

---


Head over to `http://localhost:8888` and your app should be live. 

Hit the Refresh button in the web browser to see a few more pizza images.

---


### Push your image
Now that you've created and tested your image, you can push it to [Docker Hub](https://cloud.docker.com).

First you have to login to your Docker Cloud account, to do that:

```bash
docker login
```
Enter `YOUR_USERNAME` and `password` when prompted. 

Now all you have to do is:

```bash
docker push YOUR_USERNAME/myfirstapp
```

---



Now that you are done with this container, stop and remove it... locally:

```bash
$ docker stop myfirstapp
$ docker rm myfirstapp
```
