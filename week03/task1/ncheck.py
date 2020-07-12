# -*- coding:utf-8 -*-
import random
import threading
import time
import sys
import re
import os
import socket
from requests.cookies import RequestsCookieJar
from queue import Queue
from netaddr import IPNetwork, IPRange

port_start = 1
port_end = 8000
lock = threading.Lock()
portQueue = Queue()  # 存放解析数据的queue
ping_result = {
    "ping_pass": [],
    "ping_fail": []
}
tcp_result = {}
flag = False


class InputError(BaseException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        print(self.message)
        return ("输入参数有误，使用方法示例：pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100")


class PingThread(threading.Thread):
    '''
    爬虫类
    '''

    def __init__(self, thread_id, queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        '''
        重写run方法
        '''
        # print(f'启动ping线程：{self.thread_id}')
        self.scheduler()
        # print(f'结束ping线程：{self.thread_id}')

    # 模拟任务调度
    def scheduler(self):
        while True:
            time.sleep(random.randint(1, 5))
            if self.queue.empty():  # 队列为空不处理
                break
            else:
                ipaddr = self.queue.get()
                backinfo = os.system('ping -w 2 -n 1 %s >nul' % ipaddr)
                lock.acquire()
                if backinfo == 0:
                    ping_result['ping_pass'].append(ipaddr)
                    print(f"ping {ipaddr} pass")
                else:
                    ping_result['ping_fail'].append(ipaddr)
                    # print(f"ping {ipaddr} fail")
                lock.release()
                if backinfo == 0:
                    for port in range(port_start, port_end + 1):
                        portQueue.put((ipaddr, port))


class TcpThread(threading.Thread):
    '''
    页面内容分析
    '''

    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        # print(f'启动tcp线程：{self.thread_id}')
        while True:
            try:
                item = self.queue.get(False)  # 参数为false（非阻塞）时队列为空，抛出异常
                if item is None:
                    # print(f'结束tcp线程：{self.thread_id}')
                    break
                ipaddr = item[0]
                ipport = item[1]

                self.scan_port(ipaddr, ipport)
                self.queue.task_done()  # get之后检测是否会阻塞
            except Exception as e:
                pass
            time.sleep(0.5)

    def scan_port(self, ipaddr, port):
        try:
            res = socket.create_connection((ipaddr, port), timeout=3)
            res.close()
            print("%s - %d port is open" % (ipaddr, port))
            status = True
        except socket.error as e:
            status = False
        lock.acquire()
        if status:
            if ipaddr not in tcp_result:
                tcp_result[ipaddr] = {"open_port": []}
            tcp_result[ipaddr]["open_port"].append(port)
        lock.release()


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
    ip_str = param_list[6]
    print(ip_str)
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


def check_ip(ipAddr):
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False


if __name__ == '__main__':
    thread_list = []
    try:
        thread_num, mode, ip_list = check_input(sys.argv)
    except InputError as e:
        print(e)
        sys.exit(1)
    print(f'共要检测{len(ip_list)}个ip地址')
    pingQueue = Queue()
    for ipaddr in ip_list:
        pingQueue.put(ipaddr)
    print("---------------检测开始------------------")

    # ping线程
    ping_threads = []
    for thread_id in range(thread_num):
        thread = PingThread(thread_id, pingQueue)
        thread.start()
        ping_threads.append(thread)

    # tcp线程
    tcp_threads = []
    for thread_id in range(thread_num):
        thread = TcpThread(thread_id, portQueue)
        thread.start()
        tcp_threads.append(thread)

    # 结束ping线程
    for t in ping_threads:
        t.join()
    for i in range(thread_num):
        portQueue.put(None)

    # 结束tcp线程
    for t in tcp_threads:
        t.join()

    # 重新排序
    ping_result['ping_pass'] = sorted(ping_result['ping_pass'])
    ping_result['ping_fail'] = sorted(ping_result['ping_fail'])
    for ipaddr, port_dict in tcp_result.items():
        port_dict["open_port"] = sorted(port_dict["open_port"])

    # 输出结果
    print(ping_result)
    print(tcp_result)
