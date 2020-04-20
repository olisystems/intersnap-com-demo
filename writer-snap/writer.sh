#! /bin/sh

[ -e "$SNAP_DATA/config.toml" ] || touch $SNAP_DATA/config.toml

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

exec "$@"