from __future__ import absolute_import

import json
import unittest

from celeryapp import app
from celery import chain
from celery.result import AsyncResult

import workflow.tasks as t

class Workflow(object):
    def __init__(self, jsonstr):
        self.tasks = json.loads(jsonstr)
        self.completed = []

    def run(self):
        chain(getattr(t, task['name'] + '_start').si(*task['params']) for task in self.tasks)()

    def undo_last(self):
        last = self.completed.pop()
        getattr(t, last['name'] + '_undo').delay(last['params'])

    def undo_all(self):
        self.completed.reverse()
        chain(getattr(t, task['name'] + '_undo').si(*task['params']) for task in self.completed)()

        del self.completed[:]

class testWorkflow(unittest.TestCase):
    def setUp(self):
        jsonfile = 'example.json'
        with open(jsonfile) as f:
            json = f.read()
            self.workflow = Workflow(json)

        self.assertEqual(len(self.workflow.tasks), 2)

    def test_run(self):
        self.assertFalse(self.workflow.completed)
        self.workflow.run()
        self.assertTrue(self.workflow.completed)

    def test_undo_last(self):
        self.workflow.run()
        self.workflow.undo_all()
        self.assertFalse(self.workflow.completed)

    def test_undo_all(self):
        self.workflow.run()
        self.workflow.undo_all()
        self.assertFalse(self.workflow.completed)

if __name__ == '__main__':
    unittest.main()
