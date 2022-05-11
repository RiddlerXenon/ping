from ipaddress import IPv4Network

import main

def mask_calc(ip, mask):
    net = IPv4Network((ip, mask))
    hosts = list(net.hosts())

    main.do_schedule(hosts)