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

    def trail(self, task):
        while task.parent:
            yield task
            task = task.parent
        yield task

    def run(self):
        c = chain(getattr(t, task['name']).si(**task['params']) for task in self.tasks)()

        try:
            c.get()
        finally:
            succeeded = [task for task in reversed(list(self.trail(c))) if task.status == "SUCCESS" or task.status == "FAILURE"]
            self.completed = self.tasks[:len(succeeded)]

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
        failingjsonfile = 'failingexample.json'
        with open(jsonfile) as f:
            json = f.read()
            self.workflow = Workflow(json)

        with open(failingjsonfile) as f:
            json = f.read()
            self.failingworkflow = Workflow(json)

    def test_run(self):
        self.assertFalse(self.workflow.completed)
        self.workflow.run()
        self.assertTrue(self.workflow.completed)

    def test_run_failing(self):
        self.assertRaises(ValueError, self.failingworkflow.run)

    def test_undo_last(self):
        self.assertRaises(ValueError, self.failingworkflow.run)
        self.assertTrue(self.failingworkflow.completed)
        beforeUndo = len(self.failingworkflow.completed)
        self.failingworkflow.undo_last()
        self.assertEqual(len(self.failingworkflow.completed), beforeUndo-1)

    def test_undo_all(self):
        self.assertRaises(ValueError, self.failingworkflow.run)
        self.assertTrue(self.failingworkflow.completed)
        self.failingworkflow.undo_all()
        self.assertFalse(self.failingworkflow.completed)

if __name__ == '__main__':
    unittest.main()
