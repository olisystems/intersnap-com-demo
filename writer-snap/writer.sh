#! /bin/sh

[ -e "$SNAP_COMMON/config.toml" ] || touch $SNAP_COMMON/config.toml

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

exec "$@"