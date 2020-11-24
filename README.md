# flask-uwsgi-nginx-postgres-on-K8
Running Flask app with uwsgi, nginx, and postgres on Kubernetes cluster 

**Requirements:**
1. A working Kubernetes cluster with ingress controller (in this set up, we used HAproxy). For how to launch a Kubernetes on AWS using Terraform please look at this repo: [launch Kubernetes cluster in AWS with Terraform.](https://github.com/zeebote/create-kubernetes-cluster-on-aws-with-terraform)  
1.Flask app (I use the Flaskr app in Flask Pallet Project tutorials with s few modification to make it work with Postgres. For detail please use following [link](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
1. uWSGI for serving Flask app, for more info on uWSGI please follow this [link](https://uwsgi-docs.readthedocs.io/en/latest/)
1. Docker - use to build container for Flask, Postgres, and Nginx containers. For more infomation how to install Docker please follow this [link](https://docs.docker.com/engine/install/)

**How to use:**
1. Clone this repo to your workspace
1. Deploy Postgres to Kubernetes - We use official Postgress container on Docker hub - This deployment will create a namespace "flaskr", a persistent nfs volume, 
a persitent volume claim, configmap, service, secret (for postgress user and password), and a pod which host postgres container. For this setup we postgress as user name and password for database. You should change them and convert to base64 encoding then update to deployment secret.
1. Build Flask app container
   Tag images and push to docker hub account
   
1. Deploy Flask app to Kubernetes - Before deploy make sure update configmap and secret data  
1. Build Nginx container - Before deploy nginx, you need to update the ingress with the correct FQDN to server for your app
   Tag image amd push to docker hub
1. Deploy Nginx to Kubernetes
   Verify on Kubernetes
1. Initilize Flask app database 
1. Verify if the app is working. 
1. Final step? Monitoring uWSGI, Nginx
   The app is including exporter for uWSGI, and Nginx for Prometheus to scape the status.  
