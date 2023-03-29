import time
import os
import glob
from apply_async import apply_async


def foo(fname: str) -> int:
    time.sleep(0.1)
    return len(fname)


def main() -> None:
    fnames = glob.glob(f"{os.path.expanduser('~')}/**/**")
    r = apply_async(
        fnames,
        foo,
        batch_size=10,
        nproc=10,
        update_every=1,
        refresh_per_second=10,
        timeout=0.3,
    )
    print(r)


if __name__ == "__main__":
    main()
