from ipaddress import IPv4Network

import main

def mask_calc(ip, mask):
    count = 0
    dl = ''

    for i in range(1, len(ip)):
        if ip[-i] != '.':
            count += 1
        else:
            dl = ip[:(len(ip) - count)]
            break

    net = IPv4Network((ip, mask))
    hosts = list(net.hosts())

    main.do_schedule(dl, int(str(hosts[0]).replace(dl, '')), int(str(hosts[-1]).replace(dl, '')) + 1)