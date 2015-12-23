## Restore file mode for git repositories
If for some reason all the file modes changed on your local copy of a git repository (maybe you copied your entire code folder to a NTFS partition:|), you can use this code to crawl recursively on a folder containing your repositories, and it will restore the previous file mode (according to git diff).

To run:
`python fix-mode.py <folder_path>`

Optionally, you can run with the flag -d in order to perform a dry run (doesn't change files' modes, only prints what would be changed.)