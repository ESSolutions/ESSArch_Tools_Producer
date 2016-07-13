from __future__ import absolute_import

import json
import unittest

from celeryapp import app
from celery import chain
from celery.result import AsyncResult

import workflow.tasks as wt


class Workflow(object):
    def __init__(self, jsonstr):
        self.tasks = json.loads(jsonstr)
        self.completed = []

    def add_task(self, name, params, index=None):
        idx = index or len(self.tasks)
        self.tasks.insert(idx, {
            "name": name,
            "params": params
        })

    def trail(self, task):
        while task.parent:
            yield task
            task = task.parent
        yield task

    def run(self):
        c = chain(getattr(wt, task['name']).si(**task['params']) for task in self.tasks)()

        try:
            c.get()
        finally:
            comp = [t for t in reversed(list(self.trail(c))) if t.status == "SUCCESS" or t.status == "FAILURE"]
            self.completed = self.tasks[:len(comp)]

    def undo_last(self):
        last = self.completed.pop()
        getattr(wt, last['name'] + '_undo').delay(**last['params'])

    def undo_all(self):
        self.completed.reverse()
        chain(getattr(wt, task['name'] + '_undo').si(**task['params']) for task in self.completed)()

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

    def test_add_task(self):
        name = "added"
        params = {
            "foo": "bar"
        }

        before = len(self.workflow.tasks)
        idx = 1

        self.workflow.add_task(name, params, index=idx)

        self.assertEqual(before+1, len(self.workflow.tasks))
        self.assertEqual(self.workflow.tasks[idx]["name"], name)
        self.assertEqual(self.workflow.tasks[idx]["params"], params)

        self.workflow.add_task(name, params)
        self.assertEqual(self.workflow.tasks[-1]["name"], name)
        self.assertEqual(self.workflow.tasks[-1]["params"], params)

if __name__ == '__main__':
    unittest.main()
