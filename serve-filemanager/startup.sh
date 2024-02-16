#!/bin/ash

/filebrowser config init
/filebrowser users add $FB_USERNAME $FB_PASSWORD
/filebrowser config set --branding.name "Serve File Manager" --branding.files "/home/serve/branding" --branding.disableExternal
/filebrowser config set --auth.method=noauth
/filebrowser
