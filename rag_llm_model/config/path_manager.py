from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class PathManager():
    ROOT : Path = Path.cwd()
    DATA : Path = ROOT / 'src' / 'data'
    AUDIO : Path = DATA / 'audio'
    PDF: Path = DATA / 'pdf'
    DOCX : Path = DATA / 'word'
    TEXT: Path = DATA / 'text'


if __name__ == "__main__":
    print(PathManager.ROOT)
    print(PathManager.DATA)
    print(PathManager.AUDIO)
    print(PathManager.DOCX)