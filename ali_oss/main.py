import oss2
import os
from config import common_setting
from config import oss_setting
import utils as ali_utils
import db
from datetime import timedelta


def get_all_file_folders(dest_dir):
    file_list = []
    foler_list = []

    def get_all(dest_dir):
        item_list = os.listdir(dest_dir)
        import pdb;pdb.set_trace()
        for item in item_list:
            if os.path.isdir(dest_dir + '\\' + item):
                item_dic = {}
                item_dic['name'] = item
                item_dic['url'] = dest_dir + '\\' + item
                item_dic['type'] = 'folder'
                item_dic['hash'] = ali_utils.get_hash(item_dic['name'],
                                                      item_dic['url'])
                foler_list.append(item_dic)
                get_all(item_dic['url'])
            else:
                item_dic = {}
                item_dic['name'] = item
                item_dic['url'] = dest_dir + '\\' + item
                item_dic['type'] = 'file'
                item_dic['hash'] = ali_utils.get_hash(item_dic['name'],
                                                      item_dic['url'])
                file_list.append(item_dic)
    get_all(dest_dir)
    for file in file_list:
        print('('+"'"+file['name']+"'"+',' + "'"+file['url']+"'" + ',' \
              + "'" + file['type']+"'"+',' + "'"+file['hash']+"'"+')')
    return {'file_list': file_list, 'foler_list': foler_list}


def get_endpoint(protocol, region, domain):
    return protocol + "://" + region + "." + domain


def get_bucket():
    auth = oss2.Auth(oss_setting.AccessKeyID, oss_setting.AccessKeySecret)
    endpoint = get_endpoint(oss_setting.protocol,
                            oss_setting.regions['huadong-2'],
                            oss_setting.domain)
    return oss2.Bucket(auth, endpoint, oss_setting.bucketname)


def check_status():
    remote_db = common_setting.dest_dir + "/boot.db"
    local_db = common_setting.dest_dir + '/bootnote.db'
    if db.get_timestamp(remote_db) - \
            db.get_timestamp(local_db) > timedelta(minutes=0):
        return "download"
    elif db.get_timestamp(remote_db) - \
            db.get_timestamp(local_db) < timedelta(minutes=0):
        return "upload"
    else:
        return "donothing"


def get_download_targets():    
    bucket = get_bucket()
    remote_db = common_setting.dest_dir + "/boot.db"
    local_db = common_setting.dest_dir + '/bootnote.db'
    bucket.get_object_to_file('bootnote.db', remote_db)
    remotedb_items = db.get_all_from_db(remote_db)
    localdb_items = db.get_all_from_db(local_db)
    return ali_utils.get_changed_list(localdb_items, remotedb_items)


def start_synchronization():
    status = check_status()
    if status == "download":
        write_list, update_list = get_download_targets()
        downloaded_targets = dowload(targets)
        write(downloaded_targets)
        update_local_db()
        ali_utils.sleep_min(30)
    elif status == "upload":
        targets = get_targets()
        upload(targets)
        ali_utils.sleep_min(30)
    else:
        return


def start_saving(dest_url, db_url):
    item_list = get_all_file_folders(dest_url)
    db_item_list = db.get_all_from_db(db_url)
    save_list, update_list = ali_utils.get_changed_list(item_list,
                                                        db_item_list)
    db.save_to_db(save_list)
    db.update_to_db(update_list)
    

def main():
    # while(1):      
        # start_synchronization()
        # start_saving()
    get_all_file_folders(common_setting.dest_dir)
                

if __name__ == "__main__":
    main()


