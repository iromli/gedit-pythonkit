#!/usr/bin/env bash

PYTHONKIT=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
GEDIT_PLUGIN_DIR=~/.gnome2/gedit/plugins

echo "installing pythonkit plugin"
if [[ ! -d $GEDIT_PLUGIN_DIR ]]; then
    mkdir -p $GEDIT_PLUGIN_DIR
fi
cp -R $PYTHONKIT/plugin/pythonkit* $GEDIT_PLUGIN_DIR
