import hashlib
import os
import time


def get_hash(name, url):
    if os.path.isdir(url):
        return hashlib.sha256(name).hexdigest()
    else:
        with open(url, 'r') as f:
            content = f.read()
        if content is not None:
            return hashlib.sha256(content).hexdigest()


def sleep_min(min):
    time.sleep(min * 60)


def get_changed_list(local_list, remote_list):
    # current conditin and db is local
    # db and bucket is remote
    write_list = []
    update_list = []
    for local in local_list:
        for remote in remote_list:
            if local['url'] == remote['url']:
                if local['hash'] != local['hash']:
                    update_list.append(local)
            write_list.append(local)
    return write_list, update_list

    