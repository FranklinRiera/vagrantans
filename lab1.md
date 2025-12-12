# **AWS**: running an HTTP App on an AWS instance
 
## 1. Create an AWS instance in EC2
 
1. Create an micro instance in AWS with a Debian image. 
2. Create and assign a private key to the instance
3. Find the assigned Public IP
4. Open the TCP ports: 80, 443, 22, 500
5. Access the instance via SSH

## 2. Create an HTTP App

The objective is to build a Python application using the Flask microframework on Debian. The majority of this tutorial will be about how to set up the [Gunicorn application server](http://gunicorn.org/) and how to launch the application and configure [Nginx](https://www.nginx.com/) to act as a front-end reverse proxy.

![Figure 1. Lab Diagram ](diagram.png)

### 2.1 Install the Components from the Debian Repositories

The first step will be to install all of required pieces from the Debian repositories. This includes `pip`, the Python package manager, which will manage the Python components. You will also get the Python development files necessary to build some of the Gunicorn components.

First, update the local package index and install the packages that will allow you to build your Python environment. These will include `python3-pip`, along with a few more packages and development tools necessary for a robust programming environment:

```bash
sudo apt update
sudo apt install python3-pip python3-dev nginx
```

### 2.2 Creating a Python Virtual Environment
Next, you’ll set up a virtual environment in order to isolate the Flask application from the other Python files on your system.

Start by installing the `python3-venv` package, which will install the `venv` module:

```bash
sudo apt install python3-venv
```

Next, make a parent directory for your Flask project. Move into the directory with the `cd` command after you create it:
```bash
mkdir ~/myproject
cd ~/myproject
```

Create a virtual environment to store your Flask project’s Python requirements by typing:

```bash
python3 -m venv myprojectenv
```

This will install a local copy of Python and  `pip`  into a directory called  `myprojectenv`  within your project directory.

Before installing applications within the virtual environment, you need to activate it. Do so by typing:

```bash
source myprojectenv/bin/activate
```

Your prompt will change to indicate that you are now operating within the virtual environment. It will look something like this:  `(myprojectenv)user@host:~/myproject$`.

## 2.3 Setting Up a Flask Application

Now that you are in your virtual environment, you can install Flask and Gunicorn and get started on designing your application.

First, install  `wheel`  with the local instance of  `pip`  to ensure that your packages will install even if they are missing wheel archives:

```bash
(myprojectenv) user@debian:~/myproject pip install wheel
```
Next, install Flask and Gunicorn:
```bash
(myprojectenv) user@debian:~/myproject pip install gunicorn flask
```

### Creating a Sample App
Now that you have Flask available, you can create a simple application. Flask is a microframework. It does not include many of the tools that more full-featured frameworks might, and exists mainly as a module that you can import into your projects to assist you in initializing a web application.

While your application might be more complex, we’ll create our Flask app in a single file, called  `myproject.py`:

```bash
(myprojectenv) user@debian:~/myproject nano myproject.py
```

The application code will live in this file. It will import Flask and instantiate a Flask object. You can use this to define the functions that should be run when a specific route is requested:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

This basically defines what content to present when the root domain is accessed. Save and close the file when you’re finished.
Now you can test your Flask app by typing:

```bash
(myprojectenv) user@debian:~/myproject python myproject.py
```
You will see output like the following, including a helpful warning reminding you not to use this server setup in production:

```bash
Output
* Serving Flask app "myproject" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Visit your server’s IP address followed by :5000 in your web browser:

```
http://your_server_ip:5000
```

When you are finished, hit `CTRL-C` in your terminal window to stop the Flask development server.

### Creating the WSGI Entry Point

Next, create a file that will serve as the entry point for your application. This will tell the Gunicorn server how to interact with the application.

Call the file  `wsgi.py`:
```bash
(myprojectenv) user@debian:~/myproject nano wsgi.py
```

In this file, import the Flask instance from our application and then run it:

```python
from myproject import app

if __name__ == "__main__":
    app.run()
```

Save and close the file when you are finished.

## 2.4 Configuring Gunicorn

Your application is now written with an entry point established. You can now move on to configuring Gunicorn.

Before moving on, check that Gunicorn can serve the application correctly.

You can do this by passing it the name of the application’s entry point. This is constructed as the name of the module (minus the  `.py`  extension), plus the name of the callable within the application. In this case, it is  `wsgi:app`.

Also specify the interface and port to bind to using the  `0.0.0.0:5000`  argument so that the application will be started on a publicly available interface:

```bash
(myprojectenv) user@debian:~/myproject gunicorn --bind 0.0.0.0:5000 wsgi:app
```
You should see output like the following:

```bash
(myprojectenv) user@debian:~/myproject gunicorn --bind 0.0.0.0:5000 wsgi:app
[2023-11-15 15:46:34 -0500] [85211] [INFO] Starting gunicorn 21.2.0
[2023-11-15 15:46:34 -0500] [85211] [INFO] Listening at: http://0.0.0.0:5000 (85211)
[2023-11-15 15:46:34 -0500] [85211] [INFO] Using worker: sync
[2023-11-15 15:46:34 -0500] [85212] [INFO] Booting worker with pid: 85212
```
Visit your server’s IP address with `:5000` appended to the end in your web browser again:
```
http://your_server_ip:5000
```

When you have confirmed that it’s functioning properly, press  `CTRL-C`  in your terminal window.

When you are done using the virtual environment, you can deactivate it:
```bash
(myprojectenv) user@debian:~/myproject deactivate
```

Any Python commands will now use the system’s Python environment again.

Next, create the **systemd service** unit file. Creating a systemd unit file will allow Debian’s init system to automatically start Gunicorn and serve the Flask application whenever the server boots.

Create a unit file ending in  `.service`  within the  `/etc/systemd/system`  directory to begin:

```bash
sudo nano /etc/systemd/system/myproject.service
```
Inside, you’ll start with the `[Unit]` section, which is used to specify metadata and dependencies. Add a description of your service here and tell the init system to only start this after the networking target has been reached:

```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target
```
Next, add a `[Service]` section. This will specify the user and group that you want the process to run under. Give your regular user account ownership of the process since it owns all of the relevant files. Also give group ownership to the `www-data` group so that Nginx can communicate easily with the Gunicorn processes. Remember to replace the username here with your username:

```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=user
Group=www-data
```
Next, map out the working directory and set the  `PATH`  environmental variable so that the init system knows that the executables for the process are located within our virtual environment. Also specify the command to start the service. This command will do the following:

-   Start 3 worker processes (though you should adjust this as necessary)
-   Create and bind to a Unix socket file,  `myproject.sock`, within our project directory. We’ll set an umask value of  `007`  so that the socket file is created giving access to the owner and group, while restricting other access
-   Specify the WSGI entry point file name, along with the Python callable within that file (`wsgi:app`)

Systemd requires that you give the full path to the Gunicorn executable, which is installed within your virtual environment.

Remember to replace the username and project paths with your own information:

```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/myproject
Environment="PATH=/home/user/myproject/myprojectenv/bin"
ExecStart=/home/user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
```
Finally, add an `[Install]` section. This will tell systemd what to link this service to if you enable it to start at boot. You’ll want this service to start when the regular multi-user system is up and running:
```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/myproject
Environment="PATH=/home/user/myproject/myprojectenv/bin"
ExecStart=/home/user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

With that, your systemd service file is complete. Save and close it now.

You can now start the Gunicorn service that you created and enable it so that it starts at boot:

```bash
sudo systemctl start myproject
sudo systemctl enable myproject
```

Let’s check the status:

```bash
sudo systemctl status myproject
```

```bash
sudo systemctl status myproject
● myproject.service - Gunicorn instance to serve myproject
● myproject.service - Gunicorn instance to serve myproject
     Loaded: loaded (/etc/systemd/system/myproject.service; enabled; preset: enabled)
     Active: active (running) since Wed 2023-11-15 15:53:34 -05; 2s ago
   Main PID: 93878 (gunicorn)
      Tasks: 4 (limit: 1099)
     Memory: 55.6M
        CPU: 267ms
     CGroup: /system.slice/myproject.service
             ├─93878 /home/user/myproject/myprojectenv/bin/python3 /home/user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m >
             ├─93881 /home/user/myproject/myprojectenv/bin/python3 /home/user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m >
             ├─93882 /home/user/myproject/myprojectenv/bin/python3 /home/user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m >
             └─93883 /home/user/myproject/myprojectenv/bin/python3 /home/user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m >

Nov 15 15:53:34 debian12 systemd[1]: Started myproject.service - Gunicorn instance to serve myproject.
```
If you see any errors, be sure to resolve them before continuing with the tutorial.

## 2.5 Configuring Nginx to Proxy Requests

Your Gunicorn application server should now be up and running, waiting for requests on the socket file in the project directory. Now you can configure Nginx to pass web requests to that socket by making some small additions to its configuration file.

Begin by creating a new server block configuration file in Nginx’s  `sites-available`  directory. Call this  `myproject`  to keep in line with the rest of the guide:

```bash
sudo rm /etc/nginx/sites-enable/default
sudo nano /etc/nginx/sites-available/myproject
```

Open up a server block and tell Nginx to listen on the default port `80`:

```bash
server {
    listen 80;
}
```


Next, add a location block that matches every request. Within this block, you’ll include the `proxy_params` file that specifies some general proxying parameters that need to be set. You’ll then pass the requests to the socket you defined using the `proxy_pass` directive:

```bash
server {
    listen 80;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/myproject/myproject.sock;
    }
}
```
Save and close the file when you’re finished.

To enable the Nginx server block configuration you’ve just created, link the file to the  `sites-enabled`  directory:
```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

With the file in that directory, you can test for syntax errors:

```bash
sudo nginx -t
```

If this returns without indicating any issues, restart the Nginx process to read the new configuration:

```bash
sudo systemctl restart nginx
```
You should now be able to navigate to your server’s Public IP in your web browser:

```
http://Public_IP
```

> **Note**: You will receive an HTTP 502 gateway error if Nginx cannot access gunicorn’s socket file. Usually this is because the user’s home directory does not allow other users to access files inside it.
If your socket file is called  `/home/user/myproject/myproject.sock`, ensure that  `/home/user`  has a minimum of  `0755`  permissions. You can use a tool like  `chmod`  to change the permissions like this:
>```bash
>sudo chmod 755 /home/sammy
>```
> Then reload the page to see if the HTTP 502 error goes away.

If you encounter any errors, trying checking the following:
-   `sudo less /var/log/nginx/error.log`: checks the Nginx error logs.
-   `sudo less /var/log/nginx/access.log`: checks the Nginx access logs.
-   `sudo journalctl -u nginx`: checks the Nginx process logs.
-   `sudo journalctl -u  myproject`: checks your Flask app’s Gunicorn logs.
