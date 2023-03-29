import time
import os
import glob
from apply_async import apply_async


def foo(_: str) -> None:
    time.sleep(0.1)


def main() -> None:
    fnames = glob.glob(f"{os.path.expanduser('~')}/**/**")
    print(f"Processing {len(fnames)} files")
    apply_async(
        fnames, foo, batch_size=10, nproc=10, update_every=1, refresh_per_second=10
    )


if __name__ == "__main__":
    main()
