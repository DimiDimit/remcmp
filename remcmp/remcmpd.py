import abc
import dataclasses
import typing


class Path(abc.ABC):
    def __repr__(self):
        return self.name
    
    @property
    @abc.abstractmethod
    def path(self) -> str:
        pass
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass


class File(Path):
    @property
    @abc.abstractmethod
    def tmp_file_msg(self) -> typing.Optional[str]:
        """e.g. ``"Downloading"``"""
        pass
    
    @abc.abstractmethod
    def get_tmp_file(self) -> typing.BinaryIO:
        pass


class Directory(Path):
    @abc.abstractmethod
    def list(self) -> typing.List[Path]:
        """Remember to filter out ``.`` and ``..``!"""
        pass
    
    @abc.abstractmethod
    def get_sub_path(self, path: str) -> Path:
        pass


@dataclasses.dataclass
class Stat:
    summary: str
    explanation: str
    times: int = 0