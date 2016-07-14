from __future__ import absolute_import

from workflow.celeryapp import app
from workflow.dbtask import DBTask

import time

@app.task
def prepareip(map_structure=None):
    print "starting, prepare IP"
    return 1

@app.task
def prepareip_undo(map_structure=None):
    print "undoing, delete dirs"
    return 2

@app.task
def generateipmetadata(premis = False):
    print "starting, generateXML" + " with premis" if premis else ""
    if premis is False:
        raise ValueError
    return 3

class Sleepy(DBTask):
    def run(self, foo):
        print "running task"
        print foo
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


@app.task
def generateipmetadata_undo(premis = False):
    print "undoing, remove XML files"
    return 4
