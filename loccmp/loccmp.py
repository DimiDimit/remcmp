import pathlib
import typing

import remcmp


class LocalPath(remcmp.Path):
    def __init__(self, path: pathlib.Path):
        self._path = path
    
    @property
    def path(self) -> str:
        return self._path.as_posix()
    
    @property
    def name(self) -> str:
        return self._path.name


class LocalFile(LocalPath, remcmp.File):
    @property
    def tmp_file_msg(self) -> None:
        return None
    
    def get_tmp_file(self) -> typing.BinaryIO:
        return self._path.open("rb")


class LocalDirectory(LocalPath, remcmp.Directory):
    def list(self) -> typing.List[LocalPath]:
        return [create_local_path(f) for f in self._path.iterdir()]
    
    def get_sub_path(self, path: str) -> remcmp.Path:
        return create_local_path(self._path.joinpath(path))


# noinspection PyUnusedLocal
def create_local_path(path: typing.Union[str, pathlib.Path], check_exists: bool = False, *args) -> \
        typing.Union[LocalFile, LocalDirectory]:
    if isinstance(path, str):
        path = pathlib.Path(path)
    if check_exists and not path.exists():
        raise FileNotFoundError(2, "No such file or directory", path.as_posix())
    if path.is_dir():
        return LocalDirectory(path)
    else:
        return LocalFile(path)


create_path = create_local_path
