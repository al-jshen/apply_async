import time
import os
import glob
from apply_async import apply_async


def foo(fname: str) -> int:
    time.sleep(0.005)
    return len(fname)


def main() -> None:
    fnames = glob.glob(f"{os.path.expanduser('~')}/**/**/**")
    print(len(fnames))
    r = apply_async(
        fnames,
        foo,
        batch_size=20,
        progress=True,
        nproc=10,
        update_every=1,
        refresh_per_second=0.5,
        timeout=1,
    )
    print(r)


if __name__ == "__main__":
    main()
