# -*- coding: utf-8 -*-

import unittest

from oscillo import app


class TestApp(unittest.TestCase):

    def test_get_commands(self):
        commands_str = ["c1:f1", "c2: curl http://localhost"]
        commands = app.get_command_list(commands_str)

        self.assertEqual([{'name': 'c1', 'cmd': 'f1'}, {'name': 'c2', 'cmd': 'curl http://localhost'}], commands)
