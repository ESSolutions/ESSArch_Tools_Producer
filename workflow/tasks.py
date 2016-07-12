from __future__ import absolute_import

from celery import shared_task

#from sip_generator import prepareIP

@shared_task
def prepareip_start(map_structure):
    print "starting, prepare IP"
    pass


@shared_task
def prepareip_undo(map_structure):
    print "undoing, delete dirs"
    pass

#from xml_generator import XMLGenerator

@shared_task
def generateipmetadata_start(premis = False):
    print "starting, generateXML" + " with premis" if premis else ""
    pass


@shared_task
def generateipmetadata_undo(premis = False):
    print "undoing, remove XML files"
    pass
