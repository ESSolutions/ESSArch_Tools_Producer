from __future__ import absolute_import

import time

from preingest.dbtask import DBTask

class Sleepy(DBTask):
    def run(self, foo=None):
        print "run task with id {}".format(self.request.id)
        self.set_progress(0, total=5)
        time.sleep(1)
        self.set_progress(1, total=5)
        time.sleep(1)
        self.set_progress(2, total=5)
        time.sleep(1)
        self.set_progress(3, total=5)
        time.sleep(1)
        self.set_progress(4, total=5)
        time.sleep(1)
        self.set_progress(5, total=5)
        return foo

    def undo(self, foo=None):
        print "undoing task with id {}".format(self.request.id)


class First(DBTask):
    def run(self, foo=None):
        print "run task with name {} and id {}".format(self.__name__, self.request.id)
        return foo

    def undo(self, foo=None):
        print "undo task with name {} and id {}".format(self.__name__, self.request.id)

class Second(DBTask):
    def run(self, foo=None):
        print "run task with name {} and id {}".format(self.__name__, self.request.id)
        return foo

    def undo(self, foo=None):
        print "undo task with name {} and id {}".format(self.__name__, self.request.id)

class Third(DBTask):
    def run(self, foo=None):
        print "run task with name {} and id {}".format(self.__name__, self.request.id)
        return foo

    def undo(self, foo=None):
        print "undo task with name {} and id {}".format(self.__name__, self.request.id)
