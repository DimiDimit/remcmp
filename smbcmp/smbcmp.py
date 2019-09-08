import json
import logging
import pathlib
import sys
import tempfile
import typing

from smb.SMBConnection import SMBConnection

import remcmp


try:
    with open("smbconf.json") as smbconff:
        try:
            smbconf = json.load(smbconff)
            username = smbconf.get("username", "guest")
            password = smbconf.get("password", "guest")
            my_name = smbconf.get("my_name", "DimitrodAM")
            remote_name = smbconf.get("remote_name", "")
            domain = smbconf.get("domain", "")
            server_ip = smbconf["server_ip"]
            server_port = smbconf.get("server_port", 139)
        except json.decoder.JSONDecodeError as e:
            remcmp.log_colored("Malformed smbconf.json:", e.args[0])
            sys.exit(1)
        except KeyError as e:
            remcmp.log_colored("Required property", e.args[0], "not specified in smbconf.json!")
            sys.exit(1)
except FileNotFoundError:
    remcmp.log_colored("smbconf.json not present!")
    sys.exit(1)

remcmp.log("Connecting to server...", level = logging.INFO)
conn = SMBConnection(username, password, my_name, remote_name, domain)
conn.log.setLevel(logging.WARN)
if not conn.connect(server_ip, server_port):
    remcmp.log_colored("Could not connect to server at ", server_ip, ":", server_port, "!", sep = "")
    sys.exit(2)
service_name = smbconf.get("service_name")
if service_name is None:
    print("Service (share) name (service_name) not specified in smbconf.json! These were found:",
          "\n".join([s.name for s in conn.listShares()]), sep = "\n", file = sys.stderr)
    sys.exit(1)


class SMBPath(remcmp.Path):
    def __init__(self, path: typing.Union[str, pathlib.PurePosixPath]):
        if isinstance(path, str):
            path = pathlib.PurePosixPath(path)
        self._path = path
    
    @property
    def path(self) -> str:
        return self._path.as_posix()
    
    @property
    def name(self) -> str:
        return self._path.name


class SMBFile(SMBPath, remcmp.File):
    @property
    def tmp_file_msg(self) -> str:
        return "Downloading"
    
    def get_tmp_file(self) -> typing.BinaryIO:
        f = tempfile.NamedTemporaryFile()
        conn.retrieveFile(service_name, self.path, f)
        f.flush()
        return f


class SMBDirectory(SMBPath, remcmp.Directory):
    def list(self) -> typing.List[SMBPath]:
        return [create_smb_path(self._path.joinpath(p.filename)) for p in conn.listPath(service_name, self.path) if
                p.filename != "." and p.filename != ".."]
    
    def get_sub_path(self, path: str) -> SMBPath:
        return create_smb_path(self._path.joinpath(path))


# noinspection PyUnusedLocal
def create_smb_path(path: typing.Union[str, pathlib.PurePosixPath], *args) -> typing.Union[SMBFile, SMBDirectory]:
    if conn.getAttributes(service_name, path if isinstance(path, str) else path.as_posix()).isDirectory:
        return SMBDirectory(path)
    else:
        return SMBFile(path)


create_path = create_smb_path
