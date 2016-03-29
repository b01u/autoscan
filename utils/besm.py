#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
import esm

class besm(object):
    def __init__(self, search):
        self.__index = esm.Index()
        self.search = search  if type(search) is list else [search,] 
        [self.__index.enter(x) for x in search] and self.__index.fix()

    def query(self, content):
        return self.__index.query(content)

if __name__ == "__main__":
    rbesm = besm(["ss", "dd"])
    print id(rbesm)
    print rbesm.query("mysql dd")
    print id(rbesm)
    print rbesm.query("mysql ssss")
