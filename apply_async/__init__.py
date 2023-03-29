__uri__ = "http://github.com/al-jshen/gaul"
__author__ = "Jeff Shen"
__email__ = "shenjeff@princeton.edu"
__license__ = "MIT"
__version__ = "0.1.0"

__all__ = ["apply_async"]


import os
from typing import Callable, TypeVar

from multiprocess import Manager, Pool, Process
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

T = TypeVar("T")


def apply_async(
    files: list[str],
    apply_fn: Callable[[str], T],
    nproc: int = os.cpu_count(),
    batch_size: int = 1024,
    progress: bool = True,
    update_every: int = 10,
    refresh_per_second: int = 2,
) -> list[T]:
    """Apply a function to a list of files in parallel using multiprocessing.
    This is done in batches to avoid memory issues, but the final result is
    returned as a flat list.

    Parameters
    ----------
    files : list[str]
        List of files to apply the function to.
    apply_fn : fn(str) -> Any
        Function to apply to each file.
    nproc : int, optional
        Number of processes to use, by default os.cpu_count()
    batch_size : int, optional
        Number of files to process in each batch, by default 1024
    progress : bool, optional
        Whether to show a progress bar, by default True
    update_every : int, optional
        How often to update the progress bar, by default 10
    refresh_per_second : int, optional
        How often to refresh the progress bars, by default 2 times per second


    Returns
    -------
    result: list[Any]
        List of results from applying the function to each file.
    """

    m = Manager()

    q = m.JoinableQueue()
    pq = m.JoinableQueue()
    results = {}

    def make_batch(batch_names, ctr, tid, apply_fn):
        pq.put(tid)
        res = []
        for s, f in enumerate(batch_names):
            try:
                res.append(apply_fn(f))
            except:
                pass
            if s % update_every == 0:
                q.put_nowait((tid, s))
        results[ctr] = res
        q.put_nowait((tid, -1))

    def manage_bar(taskids, show_pbar):
        if show_pbar:
            with Progress(
                TextColumn("Process {task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TextColumn("({task.completed}/{task.total})"),
                "•",
                TimeRemainingColumn(),
                refresh_per_second=refresh_per_second,
            ) as progress:
                while True:
                    while not pq.empty():
                        p = pq.get()
                        if p is not None:
                            progress.add_task(p, total=taskids[p])
                        pq.task_done()

                    try:
                        t_id, step = q.get(timeout=5)
                        if t_id in progress.task_ids:
                            q.task_done()
                            if step != -1:
                                progress.update(t_id, completed=step)
                            else:
                                progress.remove_task(t_id)
                    except:
                        q.close()
                        pq.close()
                        break

        else:
            while True:
                try:
                    t_id, step = q.get(timeout=5)
                except:
                    q.close()
                    pq.close()
                    break

    ctr = 0
    procs = []
    taskids = dict()
    with Pool(nproc) as pool:
        total_batches = len(files) // batch_size + (len(files) % batch_size > 0)
        for j, i in enumerate(range(0, len(files), batch_size)):
            batch_names = files[i : i + batch_size]
            curr_size = len(batch_names)
            p = pool.apply_async(make_batch, args=(batch_names, ctr, j, apply_fn))
            procs.append(p)
            taskids[j] = f"{curr_size}/{total_batches}"
            ctr += curr_size
        pb = Process(target=manage_bar, args=(taskids, progress))
        pb.start()
        for p in procs:
            p.get()
        pb.join()
        q.join()
        pq.join()

    return [
        item
        for sublist in [results[k] for k in sorted(results.keys())]
        for item in sublist
    ]
