import time


def error(message: str) -> None:
    """Sending error into Console"""
    _T = _Ti()
    print(f"[{_T}] [Error] :: {message}")


def warn(message: str) -> None:
    """Sending warn into Console"""
    _T = _Ti()
    print(f"[{_T}] [Warning] :: {message}")


def info(message: str) -> None:
    """Sending info into Console"""
    _T = _Ti()
    print(f"[{_T}] [Info] :: {message}")


def log(message: str) -> None:
    """Sending log into Console"""
    _T = _Ti()
    print(f"[{_T}] [Log] :: {message}")


def _Ti() -> str:
    """Returns Time"""
    _T = time.localtime(time.time())
    return f"{'{:0>2}'.format(str(_T.tm_hour))}:{'{:0>2}'.format(str(_T.tm_min))}:{'{:0>2}'.format(str(_T.tm_sec))}"