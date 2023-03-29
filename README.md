# apply_async

If you have a large number of files and you need to apply a function to each of them to get some outputs, then this is for you.

This provides a function called `apply_async` which takes in a list of filenames and a function to apply, and does the following for you:

- batches the files
- applies your function to each batch asynchronously
- controls the number of batches to process at a time, and automatically adds new batches when old ones complete
- shows a progress bar for each batch
