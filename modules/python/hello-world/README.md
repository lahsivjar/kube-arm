Uses python cherrypy and flask to create a simple Hello World webserver which prints Hello World

The server is launched on port 80 and can be accessed by url /py/helloworld

To deploy on k8 cluster:
1. kubectl apply -f jarvis-kube/modules/python/hello-world/deployment/hello-world-deployment.yaml
2. kubectl apply -f jarvis-kube/modules/python/hello-world/deployment/hello-world-service.yaml
3. kubectl apply -f jarvis-kube/modules/python/hello-world/deployment/hello-world-ingress.yaml
