from file_observer import FileObserver
import sys

if len(sys.argv) != 3:
    sys.exit(1)

with open("mirror_files", "r") as f:
    files = f.readlines()


fo = FileObserver(sys.argv[1], sys.argv[2], files)
