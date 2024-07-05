from config import Config
from os import path
class File :
    def __init__(self, file : str, buffer : int, start : int, end : int, header : bytes) :
        self.file = file
        self.buf = buffer
        self.start = start
        self.end = end
        self.head = header
        self.path = Config.DEFAULTPATH
        self.gen = None

    def __iter__(self) :
        self.gen = self.getdata()
        return self

    def __next__(self) :
        return next(self.gen)

    def isfile(self) :
        return True if path.exists(self.path + "/" + self.path) else False

    def partition(self, n : int) :
        size = self.end - self.start
        part = size // n
        modu = size - (n * part)
        return part, modu

    def getdata(self) :
        with open(self.path + "/" + self.file, "rb") as file :
            while True :
                data = file.read(self.buf)
                if not data :
                    break
                yield data
