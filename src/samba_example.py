import json
import os
import traceback
from tempfile import TemporaryDirectory
from socket import gethostname

from smb.SMBConnection import SMBConnection
from smb import smb_structs

from typing import List

OSPath = str
SMB_CONNECT_PARAMS = json.loads(
    os.environ.get('SMB_CONNECT_PARAMS', {'username': '', 'password': '', 'remote_ip': '',
                                          'remote_name': '',
                                          'service_name': ''}))


def create_connect(username: str, password: str, remote_name: str, remote_ip: str, my_name: str) -> SMBConnection:
    smb_structs.SUPPORT_SMB2 = True
    conn = SMBConnection(username, password, my_name, remote_name, use_ntlm_v2=True)
    try:
        conn.connect(remote_ip, 139)  # 139=NetBIOS / 445=TCP
    except Exception as ex:
        traceback.print_exc()
    return conn


def get_files_paths(path_to_folder: OSPath) -> List[dict]:
    connect = create_connect(SMB_CONNECT_PARAMS['username'], SMB_CONNECT_PARAMS['password'],
                             SMB_CONNECT_PARAMS['remote_name'], SMB_CONNECT_PARAMS['remote_ip'],
                             my_name=gethostname())

    try:
        files = connect.listPath(SMB_CONNECT_PARAMS['service_name'], path_to_folder)
        paths = [shared_file.filename for shared_file in files if not shared_file.isDirectory]
        return paths
    except Exception as ex:
        traceback.print_exc()
    finally:
        connect.close()


def download_file(source: OSPath, destination: OSPath) -> None:
    connect = create_connect(SMB_CONNECT_PARAMS['username'], SMB_CONNECT_PARAMS['password'],
                             SMB_CONNECT_PARAMS['remote_name'], SMB_CONNECT_PARAMS['remote_ip'],
                             my_name=gethostname())

    with open(destination, 'wb') as file_obj:
        try:
            _, _ = connect.retrieveFile(SMB_CONNECT_PARAMS['service_name'], source, file_obj)
        except Exception as ex:
            traceback.print_exc()
        finally:
            connect.close()


def upload_file(source: OSPath, destination: OSPath) -> None:
    connect = create_connect(SMB_CONNECT_PARAMS['username'], SMB_CONNECT_PARAMS['password'],
                             SMB_CONNECT_PARAMS['remote_name'], SMB_CONNECT_PARAMS['remote_ip'],
                             my_name=gethostname())
    with open(source, 'rb') as file_obj:
        try:
            _ = connect.storeFile(SMB_CONNECT_PARAMS['service_name'], destination, file_obj)
        except Exception as ex:
            traceback.print_exc()
        finally:
            connect.close()


def delete_remote_file(remote_path):
    connect = create_connect(SMB_CONNECT_PARAMS['username'], SMB_CONNECT_PARAMS['password'],
                             SMB_CONNECT_PARAMS['remote_name'], SMB_CONNECT_PARAMS['remote_ip'],
                             my_name=gethostname())
    try:
        connect.deleteFiles(SMB_CONNECT_PARAMS['service_name'], remote_path)
    except Exception as ex:
        traceback.print_exc()
    finally:
        connect.close()


def create_remote_dir(remote_path):
    connect = create_connect(SMB_CONNECT_PARAMS['username'], SMB_CONNECT_PARAMS['password'],
                             SMB_CONNECT_PARAMS['remote_name'], SMB_CONNECT_PARAMS['remote_ip'],
                             my_name=gethostname())
    try:
        connect.createDirectory(SMB_CONNECT_PARAMS['service_name'], remote_path)
    except Exception as ex:
        traceback.print_exc()
    finally:
        connect.close()


def delete_remote_dir(remote_path):
    connect = create_connect(SMB_CONNECT_PARAMS['username'], SMB_CONNECT_PARAMS['password'],
                             SMB_CONNECT_PARAMS['remote_name'], SMB_CONNECT_PARAMS['remote_ip'],
                             my_name=gethostname())
    try:
        connect.deleteDirectory(SMB_CONNECT_PARAMS['service_name'], remote_path)
    except Exception as ex:
        traceback.print_exc()
    finally:
        connect.close()


if __name__ == '__main__':
    exist_remote_folder = "folder/on/remote/server"
    remote_file_list = get_files_paths(exist_remote_folder)
    new_remote_folder = "new_folder/on/remote/server"
    with TemporaryDirectory() as temp_dir:
        download_file(os.path.join(exist_remote_folder, remote_file_list[0]),
                      os.path.join(temp_dir, remote_file_list[0]))
        create_remote_dir(new_remote_folder)
        upload_file(os.path.join(temp_dir, remote_file_list[0]), os.path.join(new_remote_folder, remote_file_list[0]))
        delete_remote_file(os.path.join(new_remote_folder, remote_file_list[0]))
        delete_remote_dir(new_remote_folder)
