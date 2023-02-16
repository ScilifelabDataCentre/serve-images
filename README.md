[![Black Formatting](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/black.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/black.yml)
[![Hadolint](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/hadolint.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/hadolint.yml)
[![Serve-MLFlow workflow](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-mlflow.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-mlflow.yml)
[![Serve-Tensorflow workflow](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-tensorflow.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-tensorflow.yml)
[![Serve-JupyterLab workflow](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-jupyterlab.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-jupyterlab.yml)
[![Serve-Torchserve workflow](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-torchserve.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-torchserve.yml)
[![Serve-RStudio workflow](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-rstudio.yml/badge.svg)](https://github.com/ScilifelabDataCentre/serve-images/actions/workflows/serve-rstudio.yml)


# Serve-images

This repository handles all the images for [Serve](https://github.com/ScilifelabDataCentre/stackn). 
The pipeline for an image goes as follows:
1. Build image
2. Scan for security issues
3. If secure, run tests to make sure that the image works as expected
4. If passed, push the image to GHCR
5. Run scheduled security scans of the version of the image that is used in production by Serve. This Trivy worklow must be maintained with the current list of images.

So for instance, our torchserve image is build like this
1. Pull torchserve:latest, update system and some python versions, build image
2. Scan for security issues
3. Run tests
4. Push to GHCR

We use Trivy for security scans, black for python formatting and hadolint for linting of dockerfiles.

## Trunk based workflow
In this repo, we work [Trunk based](https://www.toptal.com/software/trunk-based-development-git-flow), which means that we bypass the dev branch.

## Folder structure
```
serve-images
│   README.md
│   .gitignore
|   .github/workflows
|   ...
|
└───dev_scripts
|   |   run_<image-name>.sh
|
└───image1
│   │   Dockerfile
│   │   run_script.sh
│   │
│   └───tests
│       │   test_files/
│       │   test_script.py
|       |   Dockerfile.test
│       │   requirements.txt
│       │   ...
│   
└───image2
│   │   Dockerfile
│   │   run_script.sh
│   │
│   └───tests
|       |   ...

```


## To use

### Build and run test in local development environments
Scripts has been created to ease the processes of building and testing the image. These are found in `dev_scripts` and can be run like this:

```
$ chmod +x ./dev_scripts/run_jupyterlab.sh
$ ./dev_scripts/run_jupyterlab.sh
```

```
$ chmod +x ./dev_scripts/run_mlflow.sh
$ ./dev_scripts/run_mlflow.sh
```

```
$ chmod +x ./dev_scripts/run_rstudio.sh
$ ./dev_scripts/run_rstudio.sh
```

```
$ chmod +x ./dev_scripts/run_torchserve.sh
$ ./dev_scripts/run_torchserve.sh
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
