import os
import time
import glob
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileObserverHandler(FileSystemEventHandler):
    def __init__(self, source_path, target_path, files):
        self.source_path = source_path
        self.target_path = target_path
        self.files = files

    def on_modified(self, event):
        for file in self.files:
            file_path_source = self.source_path + "/" + file.lstrip("/")
            file_path_target = self.target_path + "/" + file.lstrip("/")

            if file_path_source == event.src_path:
                if os.path.isfile(file_path_source):
                    content = open(file_path_source, "r")
                    with open(file_path_target, "w") as f:
                        f.writelines(content)


class FileObserver:
    def __init__(self, source_path, target_path, files) -> None:
        print("Start File Observer")
        self.source_path = source_path.rstrip("/")
        self.target_path = target_path.rstrip("/")
        self.files = files
        self.init_folder_structure()
        self.start_observer()

    def init_folder_structure(self):
        for file_path in self.files:
            file_path_source = self.source_path + "/" + file_path.lstrip("/")
            file_path_target = self.target_path + "/" + file_path.lstrip("/")
            if "*" in file_path and "." in file_path and "/" not in file_path:
                ext_split = file_path.split(".")
                if len(ext_split) != 2:
                    continue
                for file_with_ext in Path(self.source_path).rglob(file_path):
                    if os.path.isfile(file_with_ext):
                        new_target_path = str(file_with_ext).replace(
                            self.source_path, self.target_path
                        )

                        os.makedirs(os.path.dirname(new_target_path), exist_ok=True)
                        shutil.copyfile(file_with_ext, new_target_path)
                    self.files.append(str(file_with_ext).replace(self.source_path, ""))
            elif os.path.isfile(file_path_source) and os.path.exists(file_path_source):
                if os.path.exists(file_path_target):
                    if os.path.samefile(file_path_source, file_path_target):
                        continue
                    os.remove(file_path_target)
                os.makedirs(os.path.dirname(file_path_target), exist_ok=True)
                shutil.copyfile(file_path_source, file_path_target)
            else:
                print(
                    "Source file does not exist or is a directory: " + file_path_source
                )

    def start_observer(self):
        event_handler = FileObserverHandler(
            self.source_path, self.target_path, self.files
        )
        observer = Observer()
        observer.schedule(event_handler, self.source_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()
