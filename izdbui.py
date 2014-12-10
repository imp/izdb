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
        Token.Toolbar.StatusLine: 'bg:#440044 #ffffff',
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


class IZdbStatusLine(TextToolbar):
    def __init__(self):
        super(IZdbStatusLine, self).__init__(token=Token.Toolbar.StatusLine)

    def get_tokens(self, cli, width):
        self.text = '{} (width {})'.format(cli.pool, width)
        return super(IZdbStatusLine, self).get_tokens(cli, width)
