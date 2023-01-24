# serve-images
All files related to images used in Serve

## Trunk based workflow
In this repo, we work [Trunk based](https://www.toptal.com/software/trunk-based-development-git-flow). 

## To use

### To build and test in local development environments

```
$ chmod +x ./dev_scripts/run_torchserve.sh
$ ./dev_scripts/run_torchserve.sh
```

```
$ chmod +x ./dev_scripts/run_jupyterlab.sh
$ ./dev_scripts/run_jupyterlab.sh
```


## Troubleshooting

### Insufficient docker permissions - linux
In case of error messages such as

> Got permission denied while trying to connect to the Docker daemon socket.

or

> docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))

Run docker as a non-root user.

See https://docs.docker.com/engine/install/linux-postinstall/

Do not forget to switch to the docker group in every new terminal.

```
newgrp docker
```
