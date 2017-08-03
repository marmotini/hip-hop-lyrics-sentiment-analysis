import time
import http.client
import os
import urllib.request, urllib.parse, urllib.error
import socket

class Helper:
    def __init__(self):
        pass

    @staticmethod
    def write_text_file(file_name, data, perm):
        with open(file_name, perm) as text_file:
            text_file.write("%s" % data)

    @staticmethod
    def create_dir(dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    # Get url page content
    @staticmethod
    def get_page(url):
        if url is None or url.strip() is "":
            return

        time.sleep(1)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
            'content-type': "application/json",
        }

        req = urllib.request.Request(url, headers=hdr)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            print("HTTPError: Url %s Error %s" % (url, err))
        except http.client.BadStatusLine as err:
            print("BadStatusLine: Url %s Error %s. " % (url, err))
        except urllib.error.URLError as err:
            print("URLError: Url %s Error %s. " % (url, err))
        except socket.error as err:
            print("socket.error: Url %s Error %s. " % (url, err))

        return None
