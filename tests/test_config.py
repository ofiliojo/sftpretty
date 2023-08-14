'''test CnOpts.config param'''

from common import SKIP_IF_MAC, PASS, USER, USER_HOME, VFS
from pathlib import Path
from sftpretty import CnOpts, Connection


@SKIP_IF_MAC
def test_connection_with_config(sftpserver):
    '''connect to a public sftp server using OpenSSH config'''
    config = Path(f'{USER_HOME}/.ssh/config')
    config.parent.mkdir(exist_ok=True, mode=0o700)
    config.touch(exist_ok=True, mode=0o644)
    config.write_bytes(bytes((f'Host 127.0.0.1\n\t'
                              f'User {USER}').encode('utf-8')))
    cnopts = CnOpts(config=config.as_posix(), knownhosts='sftpserver.pub')
    with sftpserver.serve_content(VFS):
        with Connection(sftpserver.host, cnopts=cnopts,
                        default_path='/home/test', password=PASS) as sftp:
            assert sftp.listdir() == ['pub', 'read.me']


def test_connection_with_config_alias(sftpserver):
    '''connect to a public sftp server using OpenSSH config alias'''
    config = Path(f'{USER_HOME}/.ssh/config')
    config.parent.mkdir(exist_ok=True, mode=0o700)
    config.touch(exist_ok=True, mode=0o644)
    config.write_bytes(bytes(('Host test\n\t'
                              'Hostname 127.0.0.1\n\t'
                              'IdentityFile id_sftpretty\n\t'
                              f'User {USER}').encode('utf-8')))
    cnopts = CnOpts(config=config.as_posix(), knownhosts='sftpserver.pub')
    with sftpserver.serve_content(VFS):
        with Connection('test', cnopts=cnopts, default_path='/home/test',
                        private_key_pass=PASS) as sftp:
            assert sftp.listdir() == ['pub', 'read.me']


def test_connection_with_config_identity(sftpserver):
    '''connect to a public sftp server using an OpenSSH config identity'''
    config = Path(f'{USER_HOME}/.ssh/config')
    config.parent.mkdir(exist_ok=True, mode=0o700)
    config.touch(exist_ok=True, mode=0o644)
    config.write_bytes(bytes(('Host 127.0.0.1\n\t'
                              'IdentityFile id_sftpretty\n\t'
                              f'User {USER}').encode('utf-8')))
    cnopts = CnOpts(config=config.as_posix(), knownhosts='sftpserver.pub')
    with sftpserver.serve_content(VFS):
        with Connection(sftpserver.host, cnopts=cnopts,
                        default_path='/home/test',
                        private_key_pass=PASS) as sftp:
            assert sftp.listdir() == ['pub', 'read.me']
