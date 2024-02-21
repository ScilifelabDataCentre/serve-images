#!/bin/ash

/filebrowser config init
/filebrowser users add $FB_USERNAME $FB_PASSWORD --commands "pwd,mv,ls,mkdir,cp,rm,rmdir,touch,sed,grep,cat,zip,unzip,wget,"
/filebrowser config set --branding.name "Serve File Manager" --branding.files "/home/serve/branding" --branding.disableExternal
/filebrowser config set --auth.method=noauth
/filebrowser
