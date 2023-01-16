#!/bin/bash
su rstudio-server -c "/usr/lib/rstudio-server/bin/rserver --server-daemonize=0 --server-app-armor-enabled=0"
