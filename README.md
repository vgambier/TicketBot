# TicketBot
Script that reserves one ticket on TicketSwap

Important: as mentioned in the print statements, please do not send your credit card details or do anything secure while you are behind a public proxy.

Usage:
./ticketbot.py <ticket_page_url>
The url is optional. If not specified, it will use the default url hardcoded in ticketbot.py
The first time a browser opens, you should manually log in. Afterwards, the browser should remember you.
You can run several of these in parallel, it helps offset the low speed and availability of public proxies. Convenience scripts (parallel6.sh and parallel8.sh) are included. They run 6 and 8 instances of the script respectively, and only work with the default url.

Requirements:
* selenium (pip)
* webdriver (pip)
* notify-send (package manager)
* tmux (package manager) (only needed for parallel.sh)
Because of the notify-send and paplay instructions, this only runs on Linux, but that's only for sending a system notification once a ticket has been found.

Features that are not upcoming but they would be neat in theory:
* email notifications
* use Firefox instead of Chrome
* display average effective refresh speed
