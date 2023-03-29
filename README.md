# apply_async

If you have a large number of files and you need to apply a function to each of them to get some outputs, then this is for you.

This provides a function called `apply_async` which takes in a list of filenames and a function to apply, and does the following for you:

- batches the files
- applies your function to each batch asynchronously
- controls the number of batches to process at a time, and automatically adds new batches when old ones complete
- shows a progress bar for each batch

## Installation

From pip:

```bash
pip install apply_async
```

Latest version (from source):

```bash
pip install "git+https://github.com/al-jshen/apply_async"
```

## Demo

<img width="656" alt="Screenshot 2023-03-29 at 6 26 16 PM" src="https://user-images.githubusercontent.com/22137276/228681583-98f65227-68fe-472a-a3e1-ab320bdb60cb.png">

