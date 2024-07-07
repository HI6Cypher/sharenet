from config import Config
import os
class File :
    def __init__(self, file_name : str, buffer : int, start : int, end : int) :
        self.name = file
        self.buf = buffer
        self.start = start
        self.end = end
        self._file = self.file = file
        self.path = None
        self.gen = None

    @property
    def file(self) :
        return self._file

    @file.setter
    def file(self, file_name) :
        path = Config.DEFAULTPATH + file_name
        if os.path.exists(path) :
            self.path = path
            return open(path, "rb")
        else :
            raise Exception(f"in {Config.DEFAULTPATH}, file \"{path}\" doesn't exist")

    def __iter__(self) :
        self.gen = self.getdata()
        return self

    def __next__(self) :
        return next(self.gen)

    def isfile(self) :
        return True if os.path.exists(self.path) else False

    def getsize(self) : #note : cosider that existing of self.path already checked
        size = os.getsize(self.path)
        return size

    def get_ranged_data(self) :
        ...
