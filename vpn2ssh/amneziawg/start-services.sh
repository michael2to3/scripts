#!/bin/sh

awg-quick up wg0

exec /usr/sbin/sshd -D
