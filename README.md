Access Samba/Windows Shares
Small examples how to upload, download, delete files (use at your own risk). 

Some refactoring:
- rewrite for Python 3.x
- connect parameters: dictionary from env variable
- exception handling


First you need to download these two python modules: pysmb-1.1.13 and pyasn1-0.1.7 Then extract \pysmb-1.1.13\python2\smb, \pysmb-1.1.13\python2\nmb and \pyasn1-0.1.7\pyasn1\ to the side-packages directory. After adjusting the parameters (username, password, ...) you might check for NetBIOS support or leave it for TCP support. => Port (139 = NetBIOS) and is_direct_tcp=False => SUPPORT_SMB2=True