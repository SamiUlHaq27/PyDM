import requests
from threading import Thread
from math import ceil
import os
import random
import string
from exceptions import *
import pathlib
from time import sleep


class Segments:
    def __init__(self):
        self.total = 0
        self.completed = 0

class Status:
    
    READY = 0
    STARTING = 1
    DOWNLOADING = 2
    PAUSED = 3
    RESUMING = 4
    COMPLETED = 5
    ERROR = 6

class Queue:
    
    Queues = []
    
    def __init__(self, name, max_simultaneous, chunk_size) -> None:
        self.name = name
        self.max_sim_dow = max_simultaneous
        self.max_segs = 4
        self.chunk_size = chunk_size
        self.files:list[FileDownload] = []
        self.total_files = 0
        self.downloading = 0
        self.autostart = False
        self.id = len(Queue.Queues)
        Queue.Queues.append(self)
    
    def add_file(self, url, filename, path):
        downloader = FileDownload(url, filename, path, self)
        self.files.append(downloader)

class FileData:
    
    def __init__(self, url, filename, path):
        res = requests.get(url)
        
        if res.status_code == requests.status_codes.codes.ok:
            self.id = FileData.get_id(path)
            self.filename = filename
            self.save_folder = path
            self.total_size = int(res.headers.get('Content-Length'))
            self.url = url
            self.resumeable = True if res.headers.get('Connection')=='keep-alive' else False
            self.range_unit = res.headers.get('Accept-Ranges', False)
            self.content_type = res.headers.get('Content-Type')
        else:
            raise FailedToFetch(f'Unable to fetch file error code: {res.status_code}')
    
    @staticmethod
    def get_id(path) -> str:
        '''Generates unique file name from the given path'''
        path = os.listdir(path)
        id = ''.join(random.choices(string.ascii_letters+string.digits, k=5))
        return id

class FileDownload(FileData):
    
    def __init__(self, url, filename:str, path:os.path, queue:Queue):
        super().__init__(url, filename, path)
        self.status = Status.READY
        self.segments:list[Segment] = []
        self.queue = queue
        self.completed_segments = Segments()
    
    def create_segments(self, temp_path):
        if self.range_unit:
            len_per_seg = ceil(self.total_size/self.queue.max_segs)
            start = 0
            for i in range(self.queue.max_segs):
                end = start+len_per_seg
                seg = Segment(self.url, start, end, self.range_unit, temp_path)
                self.segments.append(seg)
                start = end+1
            self.completed_segments.total = self.queue.max_segs
        else:
            seg = Segment(self.url, 0, self.total_size, self.range_unit, temp_path)
            self.segments.append(seg)
    
    def start(self, temp_path):
        self.status = Status.STARTING
        self.create_segments(temp_path)
        for seg in self.segments:
            seg.start_downloading()
    
    def pause(self):
        self.status = Status.STARTING
        for seg in self.segments:
            seg.status = Status.PAUSED
    
    def resume(self):
        self.status = Status.RESUMING
        for seg in self.segments:
            seg.pause_downloading()
    
    def save_data(self):
        data = {
            'id':self.id,
            'filename':self.filename,
            'total_size':self.total_size,
            'save_folder':self.save_folder,
            'url':self.url,
            'resumeable':self.resumeable,
            'range_unit':self.range_unit,
            'content_type':self.content_type,
            'status':self.status,
            'segments':[{
                'id':seg.id,
                'start':seg.starting,
                'end':seg.ending,
                'downloaded':seg.downloaded,
                'status':seg.status,
                'url':seg.url,
                'temp_path':seg.temp_folder
                } for seg in self.segments]
        }
        print(data)

class Segment:
    
    def __init__(self, url, start, end, range_unit, temp_path):
        self.url = url
        self.starting = start
        self.ending = end
        self.downloaded = 0
        self.total = end-start
        self.range_unit = range_unit
        self.temp_folder:os.path = temp_path
        self.id = FileData.get_id(temp_path)
        self.status = Status.READY
    
    def start_downloading(self):
        def download(self):
            self.status = Status.STARTING
            self.res = requests.get(self.url, stream=True, headers={'range':f'{self.range_unit}={self.starting}-{self.ending}'})
            with open(self.temp_folder.join(self.id), 'wb') as f:
                self.status = Status.DOWNLOADING
                for content in self.res.iter_content(chunk_size=256):
                    f.write(content)
                    self.downloaded += 256
                    if self.status == Status.PAUSED:
                        return 0
                self.status = Status.COMPLETED
        th = Thread(target=download, args=(self,), daemon=True)
        th.start()
    
    def pause_downloading(self):
        self.status = Status.PAUSED
    
    def resume(self):
        self.status = Status.RESUMING
        def download(self):
            if self.res:
                with open(self.temp_folder.join(self.id), 'ab') as f:
                    self.status = Status.DOWNLOADING
                for content in self.res.iter_content(chunk_size=256):
                    f.write(content)
                    self.downloaded += 256
                    if self.status == Status.PAUSED:
                        return 0
                self.status = Status.COMPLETED
            else:
                self.res = requests.get(self.url, stream=True, headers={'range':f'{self.range_unit}={self.starting+self.downloaded}-{self.ending}'})
                with open(self.temp_folder.join(self.id), 'ab') as f:
                    self.status = Status.DOWNLOADING
                    for content in self.res.iter_content(chunk_size=256):
                        f.write(content)
                        self.downloaded += 256
                        if self.status == Status.PAUSED:
                            return 0
                    self.status = Status.COMPLETED
        th = Thread(target=download, args=(self,), daemon=True)

if __name__=='__main__':
    queue1 = Queue('Queue 1', 2, 256)
    queue1.add_file("http://127.0.0.1:5500/Grand%20Theft%20Auto.7z", 'GTA Liberty City.7z', pathlib.Path('E:/Code/Projects/PyDM/temp'))
    queue1.files[0].start(pathlib.Path('E:/Code/Projects/PyDM/temp'))
    while(queue1.files[0].status != Status.COMPLETED):
        queue1.files[0].save_data()
        sleep(2)
        