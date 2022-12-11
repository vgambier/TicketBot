#!/bin/bash

tmux \
set-option -g remain-on-exit on \; \
new-session \
'./ticketbot.py'\; \
split-window \
'./ticketbot.py'\; \
split-window -h \
'./ticketbot.py'\; \
select-layout even-horizontal\; \
select-pane -t 0 \; \
split-window  -v \
'./ticketbot.py'\; \
select-pane -t 2 \; \
split-window  -v \
'./ticketbot.py'\; \
select-pane -t 4 \; \
split-window  -v \
'./ticketbot.py'\; \
select-pane -t 6 \; \
split-window  -v \
'./ticketbot.py'\; \
