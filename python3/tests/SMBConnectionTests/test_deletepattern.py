# -*- coding: utf-8 -*-

import os, time, random
from io import BytesIO
from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo
from nose.tools import with_setup
from smb import smb_structs

conn = None

def setup_func_SMB1():
    global conn
    smb_structs.SUPPORT_SMB2 = False

    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True)
    assert conn.connect(info['server_ip'], info['server_port'])

def setup_func_SMB2():
    global conn
    smb_structs.SUPPORT_SMB2 = True

    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True)
    assert conn.connect(info['server_ip'], info['server_port'])

def teardown_func():
    global conn
    conn.close()

@with_setup(setup_func_SMB1, teardown_func)
def test_delete_without_subfolder_SMB1():
    global conn

    path = os.sep + u'testDelete %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory('smbtest', path)

    for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
        conn.storeFile('smbtest', path+"/"+filename, BytesIO(b"0123456789"))

    for p in [ 'aaTest.Folder', 'aaTest.Folder/xyz', 'bbTest.Folder' ]:
        conn.createDirectory('smbtest', path+"/"+p)
        for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
            conn.storeFile('smbtest', path+"/"+p+"/"+filename, BytesIO(b"0123456789"))

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' in filenames
    assert 'aaBest.txt' in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aa*.txt')

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' not in filenames
    assert 'aaBest.txt' not in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aaTest.*')

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.bin' not in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames


@with_setup(setup_func_SMB1, teardown_func)
def test_delete_with_subfolder_SMB1():
    global conn

    path = os.sep + u'testDelete %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory('smbtest', path)

    for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
        conn.storeFile('smbtest', path+"/"+filename, BytesIO(b"0123456789"))

    for p in [ 'aaTest.Folder', 'aaTest.Folder/xyz', 'bbTest.Folder' ]:
        conn.createDirectory('smbtest', path+"/"+p)
        for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
            conn.storeFile('smbtest', path+"/"+p+"/"+filename, BytesIO(b"0123456789"))

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' in filenames
    assert 'aaBest.txt' in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aa*.txt', delete_matching_folders=True)

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' not in filenames
    assert 'aaBest.txt' not in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aaTest.*', delete_matching_folders=True)

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' not in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.bin' not in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames


@with_setup(setup_func_SMB2, teardown_func)
def test_delete_without_subfolder_SMB2():
    global conn

    path = os.sep + u'testDelete %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory('smbtest', path)

    for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
        conn.storeFile('smbtest', path+"/"+filename, BytesIO(b"0123456789"))

    for p in [ 'aaTest.Folder', 'aaTest.Folder/xyz', 'bbTest.Folder' ]:
        conn.createDirectory('smbtest', path+"/"+p)
        for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
            conn.storeFile('smbtest', path+"/"+p+"/"+filename, BytesIO(b"0123456789"))

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' in filenames
    assert 'aaBest.txt' in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aa*.txt')

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' not in filenames
    assert 'aaBest.txt' not in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aaTest.*')

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.bin' not in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

@with_setup(setup_func_SMB2, teardown_func)
def test_delete_with_subfolder_SMB2():
    global conn

    path = os.sep + u'testDelete %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory('smbtest', path)

    for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
        conn.storeFile('smbtest', path+"/"+filename, BytesIO(b"0123456789"))

    for p in [ 'aaTest.Folder', 'aaTest.Folder/xyz', 'bbTest.Folder' ]:
        conn.createDirectory('smbtest', path+"/"+p)
        for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
            conn.storeFile('smbtest', path+"/"+p+"/"+filename, BytesIO(b"0123456789"))

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' in filenames
    assert 'aaBest.txt' in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aa*.txt', delete_matching_folders=True)

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.txt' not in filenames
    assert 'aaBest.txt' not in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles('smbtest', path+'/aaTest.*', delete_matching_folders=True)

    results = conn.listPath('smbtest', path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.Folder' not in filenames
    assert 'bbTest.Folder' in filenames
    assert 'aaTest.bin' not in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames
