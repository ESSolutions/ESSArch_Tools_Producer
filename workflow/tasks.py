from __future__ import absolute_import

from workflow.celeryapp import app

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


@app.task
def generateipmetadata_undo(premis = False):
    print "undoing, remove XML files"
    return 4
