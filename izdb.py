#
# Copyright 2014 Cyril Plisko. All rights reserved.
# Use is subject to license terms.
#

from __future__ import print_function
from prompt_toolkit import CommandLineInterface, AbortAction, Exit
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.line import Line
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.layout.prompt import Prompt
from prompt_toolkit.layout.toolbars import TextToolbar
from pygments.styles import get_style_by_name
from pygments.styles.default import DefaultStyle
from pygments.style import Style
from pygments.token import Token

import izdbui
import libzpool

class IZdbShell(CommandLineInterface):
    def __init__(self, pool=None):
        style = izdbui.IZdbStyle
        prompt = izdbui.IZdbPrompt()
        menu = CompletionsMenu()
        layout = Layout(before_input=prompt,
                        #lexer=izdbui.ZdbLexer,
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
        self.zdb_init()

    def zdb_init(self):
        libzpool.kernel_init(libzpool.FREAD)

    def zdb_fini(self):
        libzpool.kernel_fini()

    def repl(self):
        try:
            while True:
                d = self.read_input(on_exit=self._onexit)
                print('Got', d.text)
                args = d.text.split()
                cmd = args.pop(0)
                method = getattr(self, 'do_' + cmd, None)
                if method:
                    method(self, args)
                else:
                    print('No such command', '"{}"'.format(cmd))
        except Exit:
            print('Cleaning up')
            self.zdb_fini()


def main(args):
    app = IZdbShell(pool='dpool')
    app.repl()
    return 0
