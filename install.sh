#!/usr/bin/env bash

PYTHONKIT=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
GEDIT_PLUGIN_DIR=~/.gnome2/gedit/plugins
LANGUAGE_SPEC_DIR=~/.local/share/gtksourceview-2.0/language-specs

echo "installing pythonkit plugin"
if [[ ! -d $GEDIT_PLUGIN_DIR ]]; then
    mkdir -p $GEDIT_PLUGIN_DIR
fi
cp -R $PYTHONKIT/plugin/pythonkit* $GEDIT_PLUGIN_DIR

echo "installing dtl language-spec"
if [[ ! -d $LANGUAGE_SPEC_DIR ]]; then
    mkdir -p $LANGUAGE_SPEC_DIR
fi
cp $PYTHONKIT/language-spec/dtl.lang $LANGUAGE_SPEC_DIR
