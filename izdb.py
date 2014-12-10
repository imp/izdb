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
from pygments.styles import get_style_by_name
from pygments.styles.default import DefaultStyle
from pygments.style import Style
from pygments.token import Token


class ZdbLexer(object):
    def __init__(self):
        super(ZdbLexer, self).__init__()


class ZdbCompleter(Completer):
    keywords = ['pool', 'label', 'dataset', 'mos', 'dnode', 'dir']

    def get_completions(self, doc):
        word = doc.get_word_before_cursor()

        for keyword in self.keywords:
            if keyword.startswith(word):
                yield Completion(keyword, -len(word))


class IZdbStyle(Style):
    BaseStyle = get_style_by_name('monokai')
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(BaseStyle.styles)


class IZdbPrompt(Prompt):
    def tokens(self, cli):
        if cli.pool:
            return [
                (Token.Name, cli.pool),
                (Token.Prompt, '> ')
            ]
        else:
            return [(Token.Prompt, 'izdb> ')]


class IZdbCommandLine(CommandLineInterface):
    def __init__(self, pool=None):
        style = IZdbStyle
        prompt = IZdbPrompt()
        menu = CompletionsMenu()
        layout = Layout(before_input=prompt,
                        #lexer=ZdbLexer,
                        menus=[menu])
        line = Line(completer=ZdbCompleter())
        super(IZdbCommandLine, self).__init__(layout=layout, line=line, style=style)
        self._onexit = AbortAction.RAISE_EXCEPTION
        self.debug = False
        self.readonly = True
        self.pool = pool
        self.dataset = None

    def repl(self):
        try:
            while True:
                d = self.read_input(on_exit=self._onexit)
                print('Got', d.text)
        except Exit:
            print('Cleaning up')


def main(args):
    app = IZdbCommandLine(pool='dpool')
    app.repl()
    return 0

