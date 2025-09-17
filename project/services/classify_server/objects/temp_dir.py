import tempfile, shutil

class TempDir:
    def __init__(self, prefix="tmp_"):
        self.prefix = prefix
        self.path = None

    def __enter__(self):
        self.path = tempfile.mkdtemp(prefix=self.prefix)
        return self.path

    def __exit__(self, exc_type, exc, tb):
        if self.path:
            shutil.rmtree(self.path, ignore_errors=True)
        return False