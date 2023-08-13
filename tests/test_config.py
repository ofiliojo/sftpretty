'''test CnOpts.config param'''

import pytest

from common import conn, PASS, USER, USER_HOME, VFS
from pathlib import Path
from sftpretty import CnOpts, Connection


def test_connection_with_config(sftpserver):
    '''connect to a public sftp server using OpenSSH config'''
    config = Path(f'{USER_HOME}/.ssh/config')
    config.parent.mkdir(exist_ok=True, mode=0o700)
    config.touch(exist_ok=True, mode=0o644)
    config.write_bytes(bytes(('Host localhost\n'
                              f'User {USER}').encode('utf-8')))
    cnopts = CnOpts(config=config.as_posix(),
                    knownhosts='sftpserver.pub')
    with sftpserver.serve_content(VFS):
        with Connection('localhost', cnopts=cnopts, password=PASS) as sftp:
            assert sftp.listdir() == ['pub', 'read.me']


def test_connection_with_config_alias(sftpserver):
    '''connect to a public sftp server using OpenSSH config alias'''
    config = Path(f'{USER_HOME}/.ssh/config')
    config.parent.mkdir(exist_ok=True, mode=0o700)
    config.touch(exist_ok=True, mode=0o644)
    config.write_bytes(bytes(('Host test\n'
                              'Hostname localhost\n'
                              f'User {USER}').encode('utf-8')))
    cnopts = CnOpts(config=config.as_posix(),
                    knownhosts='sftpserver.pub')
    with sftpserver.serve_content(VFS):
        with Connection('test', cnopts=cnopts, password=PASS) as sftp:
            assert sftp.listdir() == ['pub', 'read.me']


def test_connection_with_config_identity(sftpserver):
    '''connect to a public sftp server using an OpenSSH config identity'''
    config = Path(f'{USER_HOME}/.ssh/config')
    config.parent.mkdir(exist_ok=True, mode=0o700)
    config.touch(exist_ok=True, mode=0o644)
    config.write_bytes(bytes(('Host localhost\n'
                              'IdentityFile id_sftpretty\n'
                              f'User {USER}').encode('utf-8')))
    cnopts = CnOpts(config=config.as_posix(),
                    knownhosts='sftpserver.pub')
    with sftpserver.serve_content(VFS):
        with Connection('localhost', cnopts=cnopts,
                        private_key_pass=PASS) as sftp:
            assert sftp.listdir() == ['pub', 'read.me']