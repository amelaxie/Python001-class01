# -*- coding:utf-8 -*-
import socket
import sys
import os
import re
from netaddr import IPNetwork, IPRange
from concurrent.futures import ThreadPoolExecutor


class InputError(BaseException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        print(self.message)
        return ("输入参数有误，使用方法示例：pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100")


def scan_port(ipaddr, port):
    try:
        res = socket.create_connection((ipaddr, port), timeout=3)
        res.close()
        print("%s - %d port is open" % (ipaddr, port))
        return True
    except socket.error as e:
        return False


def check_ip(ipAddr):
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False


def check_input(param_list):
    if len(param_list) < 6:
        raise InputError("缺少参数")
    if param_list[1] != "-n":
        raise InputError("并发参数错误")
    try:
        thread_num = int(param_list[2])
    except:
        raise InputError("并发参数错误")
    if param_list[3] != "-f":
        raise InputError("检测参数错误")
    mode = param_list[4]
    if mode != "ping" and mode != "tcp":
        raise InputError("检测参数错误")
    ip_list = []
    ip_str = param_list[5]
    if ip_str.find("-") != -1:
        startip = ip_str.split("-")[0]
        endip = ip_str.split("-")[1]
        if not (check_ip(startip) and check_ip(endip)):
            raise InputError("ip地址参数错误")
        iprange_cidrs = IPRange(startip, endip)
        for net_cidr in iprange_cidrs.cidrs():
            for ip in net_cidr.iter_hosts():
                ip_list.append(str(ip))
    elif ip_str.find("/") != -1:
        try:
            for ip in IPNetwork(ip_str):
                ip_list.append(str(ip))
        except:
            raise InputError("ip地址参数错误")
    else:
        if not check_ip(ip_str):
            raise InputError("ip地址参数错误")
        ip_list.append(ip_str)
    return thread_num, mode, ip_list


if __name__ == '__main__':

    # ip_str = "192.168.10.0/242"
    # ip_str = "192.168.10.1-192.168.10.5"
    # try:
    #     res = IPNetwork(ip_str)
    # except  Exception as e:
    #     print type(e),e
    # ip_range = IPRange("192.168.1.10", "192.168.1.130")
    # # # 对这一段ip地址进行地址聚合
    # # #print(ip_range.cidrs())
    # for  network in ip_range.cidrs():
    #     print network
    #     for ip in network.iter_hosts():
    #         print ip


    #for ip in IPNetwork(ip_str).iter_hosts():
    #    print ip
    try:
        thread_num, mode, ip_list = check_input(sys.argv)
    except InputError as e:
        print(e)
        sys.exit(1)
    print(ip_list)
    executor = ThreadPoolExecutor(max_workers=thread_num)
    for ipaddr in ip_list:
        backinfo = os.system('ping -w 1 -n 1 %s >nul' % ipaddr)
        if backinfo == 0:
            print(ipaddr)
            for port in range(1, 8001):
                args = (ipaddr, port)
                executor.submit(lambda p: scan_port(*p), args)

# print res
