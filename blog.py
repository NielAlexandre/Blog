#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path
import urllib, ssl

from PIL import Image

#Trick for Denys bypass
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class Post:
    DICT = dict()

    def __new__(cls, filename):
        name = filename.name
        if name not in cls.DICT:
            cls.DICT[name] = inst = super().__new__(cls)
            inst._init(filename)
        inst = cls.DICT[name]
        if inst.updated:
            inst._init(filename)
        return cls.DICT[name]

    def _init(self, filename):
        self.file = Path(filename)
        self.ctime = self.file.stat().st_ctime
        self.body = list()
        self.url = None
        self.tags = ""
        self.xpos = 0
        self.loaded = False
        self.title2 = ""

        fulltext = filename.read_text()
        for l in fulltext.splitlines():
            if l.startswith('#'):
                tag, *value = l.split('=')
                setattr(self, tag.strip('#'), '='.join(value))
            else:
                self.body.append(l)
        self.tags = self.tags.split(',')


    def load_img(self):
        if not self.loaded:
            print("loading", self.file.name)
            try:
                img = Image.open(self.img)
                self.img = "/" + self.img
            except FileNotFoundError:
                try:
                    img = Image.open(urllib.request.urlopen(self.img, context=ctx))
                except urllib.error.HTTPError:
                    print("oops, no", self.img[:55],
                            ("..." if len(self.img) > 55 else ""))
                    return
                except urllib.error.URLError:
                    print("bad url", self.img)
                    return
                except ValueError:
                    return
            except AttributeError:
                return
            w, h = img.size
            w = w*(250/h)
            self.xpos = 75-w//2
        self.loaded = True

    @property
    def updated(self):
        return self.ctime != self.file.stat().st_ctime


    def __contains__(self, key):
        return key.lower() in [t.lower() for t in self.tags]

    @property
    def name(self):
        return self.title2 or self.ctime

    @property
    def title(self):
        return self.file.name

def filter_post(lst, filterin, filterout):
    for e in lst:
        if filterout and any(t in e for t in filterout):
            continue
        if not filterin:
            yield e
        elif any(t in e for t in filterin):
            yield e

def main():
    pass

if __name__ == "__main__":
    main()

