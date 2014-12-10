#
# Copyright 2014 Cyril Plisko. All rights reserved.
# Use is subject to license terms.
#

from __future__ import print_function
from prompt_toolkit import CommandLineInterface, AbortAction, Exit
from prompt_toolkit.line import Line
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu

import izdbui
import zdb

DEFAULT_ARC_SIZE = 256 * 1024 * 1024
DEFAULT_ARC_META_LIMIT = DEFAULT_ARC_SIZE


class IZdbShell(CommandLineInterface):
    def __init__(self, pool=None):
        style = izdbui.IZdbStyle
        prompt = izdbui.IZdbPrompt()
        menu = CompletionsMenu()
        layout = Layout(before_input=prompt,
                        # lexer=izdbui.ZdbLexer,
                        bottom_toolbars=[izdbui.IZdbStatusLine()],
                        menus=[menu])
        line = Line(completer=izdbui.ZdbCompleter())
        super(IZdbShell, self).__init__(layout=layout, line=line, style=style)
        self._onexit = AbortAction.RAISE_EXCEPTION
        self.debug = False
        self.readonly = True
        self.pool = pool
        self.dataset = None
        # Call ZDB
        self.zdb = zdb.Zdb(DEFAULT_ARC_SIZE, DEFAULT_ARC_META_LIMIT)
        self.zdb.zdb_init()

    def do_print(self, vars):
        _print = lambda x: print('{} = {}'.format(x, getattr(self.zdb, x)))
        try:
            [_print(var) for var in vars]
        except AttributeError as e:
            print('No variable "{}"'.format(e))

    def repl(self):
        try:
            while True:
                d = self.read_input(on_exit=self._onexit)
                args = d.text.split()
                print('Got {} ({})'.format(d.text, len(args)))
                if len(args) == 0:
                    continue
                cmd = args.pop(0)
                method = getattr(self, 'do_' + cmd, None)
                if method:
                    method(args)
                else:
                    print('No such command "{}"'.format(cmd))
        except Exit:
            print('Cleaning up')
            self.zdb.zdb_fini()


def main(args):
    app = IZdbShell(pool='dpool')
    app.repl()
    return 0
