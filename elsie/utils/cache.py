import hashlib
import os
import tempfile
import threading


class FsCache:
    def __init__(self, cache_dir, version):
        start = f"elsie-{version}/".encode()
        self.hasher = hashlib.sha1()
        self.hasher.update(start)
        self.cache_dir = cache_dir
        self.touched_files = set()
        self.cache_files = {
            filename
            for filename in os.listdir(cache_dir)
            if filename.startswith("cache.")
        }
        self.lock = threading.Lock()
        self.in_progress = {}

    def _get_filename(self, input_data, data_type):
        h = self.hasher.copy()
        if isinstance(input_data, str):
            input_data = input_data.encode()
        h.update(input_data)
        return "cache.{}.{}".format(h.hexdigest(), data_type)

    def _full_path(self, filename):
        return os.path.join(self.cache_dir, filename)

    def ensure_by_file(self, filename, data_type, constructor, wait_on_collision=True):
        with open(filename, "rb") as f:
            data = f.read()
        return self.ensure(
            data, data_type, constructor, wait_on_collision=wait_on_collision
        )

    def ensure(self, input_data, data_type, constructor, wait_on_collision=True):
        cache_file = self._get_filename(input_data, data_type)
        full_path = self._full_path(cache_file)
        with self.lock:
            self.touched_files.add(cache_file)
            condition = self.in_progress.get(cache_file)
            if condition is not None:
                if wait_on_collision:
                    condition.wait()
                    assert cache_file in self.cache_files
                return full_path
            if cache_file in self.cache_files:
                return full_path

        condition = threading.Condition(self.lock)
        self.in_progress[cache_file] = condition
        constructor(input_data, full_path, data_type)
        with self.lock:
            self.cache_files.add(cache_file)
            del self.in_progress[cache_file]
            condition.notify_all()
        return full_path

    def remove_unused(self):
        for filename in self.cache_files.difference(self.touched_files):
            os.remove(self._full_path(filename))

    def get(self, input_data, data_type, constructor):
        cache_file = self._get_filename(input_data, data_type)
        self.touched_files.add(cache_file)
        full_path = os.path.join(self.cache_dir, cache_file)

        if cache_file in self.cache_files:
            with open(full_path, "r") as f:
                return f.read()

        result = constructor(input_data)
        with open(full_path, "w") as f:
            f.write(result)
        self.cache_files.add(cache_file)
        return result


def get_cache_file_path(directory: str, extension: str) -> str:
    temp_path = os.path.abspath(
        os.path.join(directory, f"cache.{next(tempfile._get_candidate_names())}")
    )
    return f"{temp_path}.{extension}"
