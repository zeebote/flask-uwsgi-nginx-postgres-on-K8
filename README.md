# flask-uwsgi-nginx-postgres-on-K8
Running Flask app with uwsgi, nginx, and postgres on Kubernetes cluster 

**Requirements:**
1. A working Kubernetes cluster with ingress controller (in this set up, we used HAproxy). For how to launch a Kubernetes on AWS using Terraform please look at this repo: [launch Kubernetes cluster in AWS with Terraform.](https://github.com/zeebote/create-kubernetes-cluster-on-aws-with-terraform)  
1. Flask app (I use the Flaskr app in Flask Pallet Project tutorials with s few modification to make it work with Postgres. For detail please use following [link](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
1. uWSGI for serving Flask app, for more info on uWSGI please follow this [link](https://uwsgi-docs.readthedocs.io/en/latest/)
1. Docker - use to build container for Flask, Postgres, and Nginx containers. For more infomation how to install Docker please follow this [link](https://docs.docker.com/engine/install/)

**How to use:**
1. Clone this repo to your workspace
   ```
   git clone https://github.com/zeebote/flask-uwsgi-nginx-postgres-on-K8 .
   ~/blog$ tree
   ├── deployment             #Kubernetes deployment yaml files
   │   ├── flaskr.yml
   │   ├── nginx.yml
   │   └── postgres.yml
   ├── flaskr                          # Flask project folder
   │   ├── config.py
   │   ├── docker-entrypoint.sh
   │   ├── Dockerfile
   │   ├── flaskr                      #Flaskr app folder
   │   │   ├── auth.py
   │   │   ├── blog.py
   │   │   ├── db.py
   │   │   ├── flaskr.ini
   │   │   ├── __init__.py
   │   │   ├── models.py
   │   │   ├── __pycache__
   │   │   │   ├── auth.cpython-36.pyc
   │   │   │   ├── blog.cpython-36.pyc
   │   │   │   ├── db.cpython-36.pyc
   │   │   │   ├── __init__.cpython-36.pyc
   │   │   │   └── models.cpython-36.pyc
   │   │   ├── static
   │   │   │   └── style.css
   │   │   └── templates
   │   │       ├── auth
   │   │       │   ├── login.html
   │   │       │   └── register.html
   │   │       ├── base.html
   │   │       ├── base.html.org
   │   │       └── blog
   │   │           ├── create.html
   │   │           ├── index.html
   │   │           ├── index.html.org
   │   │           └── update.html
   │   ├── __pycache__
   │   │   ├── config.cpython-36.pyc
   │   │   └── wsgi.cpython-36.pyc
   │   ├── requirements.txt
   │   └── wsgi.py
   ├── nginx                           #Nginx folder
   │   ├── default.conf
   │   ├── Dockerfile
   │   └── uwsgi_params
   └── README.md
   ```
1. Deploy Postgres to Kubernetes - We use official Postgress container on Docker hub - This deployment will create a namespace "flaskr", a persistent nfs volume, a persitent volume claim, configmap, service, secret (for postgress user and password), and a pod which host postgres container. For this setup we postgress as user name and password for database. You should change them and convert to base64 encoding then update to deployment secret.
   ```
   ~/blog$ kubectl apply -f deployment/postgres.yml
   namespace/flaskr created
   persistentvolume/nfs-postgresflaskr created
   persistentvolumeclaim/postgres-pv-claim created
   service/postgres created
   configmap/postgres-config created
   secret/postgres-secret created
   deployment.apps/postgres created
   ```
1. Build Flask app container
   ```
   ~/blog$ docker build -t flaskr flaskr/
   Successfully built b948430c11c0
   Successfully tagged flaskr:latest
   ```
   Tag images and push to your docker hub account 
   ```
   ~/blog$ docker tag flaskr trucv/flaskr
   ~/blog$ docker push trucv/flaskr
   The push refers to repository [docker.io/trucv/flaskr]
   fe027389e901: Pushed
   0d92ca5c3a67: Pushed
   8d2a60deb142: Layer already exists
   162dfdb1d604: Layer already exists
   2884295f40ee: Layer already exists
   d979a769ea12: Layer already exists
   f04cc38c0ac2: Layer already exists
   ace0eda3e3be: Layer already exists
   latest: digest: sha256:fe4fd9ddb901a0c5ec01ad6ace9c22e12fe1f9ac6a60cef2cd636b55c705317b size: 1995
   ```
1. Deploy Flask app to Kubernetes - Before deploy make sure update configmap and secret data  
   ```
   ~/blog$ kubectl apply -f deployment/flaskr.yml
   configmap/flaskr-config created
   secret/flaskr-secret created
   service/flaskr created
   service/uwsgi-exporter created
   deployment.apps/flaskr created
   ```
1. Build Nginx container - Before deploy nginx, you need to update the ingress with the correct FQDN to server for your app
   ```
   ~/blog$ docker build -t nginxflaskr nginx/
   Sending build context to Docker daemon  4.608kB
   Step 1/4 : FROM nginxinc/nginx-unprivileged:1.18-alpine
    ---> 01616b00c046
   Step 2/4 : COPY ./default.conf /etc/nginx/conf.d/default.conf
    ---> Using cache
    ---> 82ad0268aca2
   Step 3/4 : COPY ./uwsgi_params /etc/nginx/uwsgi_params
    ---> Using cache
    ---> 4aad4436acae
   Step 4/4 : USER nginx
    ---> Using cache
    ---> e05004c208eb
   Successfully built e05004c208eb
   Successfully tagged nginxflaskr:latest
   ```
   Tag image amd push to docker hub
   ```
   ~/blog$ docker tag nginxflaskr trucv/nginxflaskr
   ~/blog$ docker push trucv/nginxflaskr
   The push refers to repository [docker.io/trucv/nginxflaskr]
   The push refers to repository [docker.io/trucv/nginxflaskr]
   3c5df08f4f68: Layer already exists
   85817c59d357: Layer already exists
   879506c17d96: Layer already exists
   0c65e5c392c9: Layer already exists
   3b99a838f4af: Layer already exists
   1c308a2ee825: Layer already exists
   ed295e36483a: Layer already exists
   3e207b409db3: Layer already exists
   latest: digest: sha256:9a0db2b8bea8d2445ecd4c6e5060ec4fde2b7a4d9668afd79796c4b9ae662fea size: 1982
   ```
1. Deploy Nginx to Kubernetes
   ```
   ~/blog$ kubectl apply -f deployment/nginx.yml
   service/nginx-flaskr created
   service/nginx-flaskr-exporter created
   ingress.extensions/nginx-flaskr created
   deployment.apps/nginx-flaskr created
   ```
   Verify on Kubernetes
   ```
   ~/blog$ kubectl -n flaskr get pod -o wide
   NAME                            READY   STATUS    RESTARTS   AGE     IP             NODE          NOMINATED NODE   READINESS GATES
   flaskr-66c99b64ff-ksk6p         2/2     Running   0          5m51s   10.244.64.8    moh-eng-025   <none>           <none>
   flaskr-66c99b64ff-xsg8d         2/2     Running   0          5m51s   10.244.192.7   moh-eng-002   <none>           <none>
   nginx-flaskr-7bc594fb54-tjfsh   2/2     Running   0          61s     10.244.64.9    moh-eng-025   <none>           <none>
   postgres-d667745c-frg5w         1/1     Running   0          13m     10.244.64.5    moh-eng-025   <none>           <none>
   ```
1. Initilize Flask app database 
   ```
   ~/blog$ kubectl -n flaskr exec -ti --container flaskr flaskr-66c99b64ff-ksk6p -- flask init-db
   Initialized the database
   ```
1. Verify the app, if everything is working, you should see login page. 
   ```
   curl your.flask.app.serving.com
   <!doctype html>
   <title>Posts - Flaskr</title>
   <link rel="stylesheet" href="/static/style.css">
   <nav>
     <h1>Flaskr</h1>
     <ul>
         <li><a href="/auth/register">Register</a>
         <li><a href="/auth/login">Log In</a>
     </ul>
   </nav>
   <section class="content">
     <header>
     <h1>Posts</h1>
     </header>
   ```
1. Final step? Monitoring uWSGI, Nginx

   The app is including exporter for uWSGI, and Nginx for Prometheus to scape the status.  
