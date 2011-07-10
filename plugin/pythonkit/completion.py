# -*- coding: utf-8 -*-

# Gedit PythonKit plugin
# Copyright 2011 Isman Firmansyah <izman.romli@gmail.com>

import gobject
import gtksourceview2 as gsv
import re
from gettext import gettext as _
from parser import complete as python_complete


class PythonProposal(gobject.GObject, gsv.CompletionProposal):

    def __init__(self, proposal):
        gobject.GObject.__init__(self)
        self.abbr = proposal['abbr']
        self.word = proposal['word']
        self.info = proposal['info']

    def do_get_text(self):
        return self.word

    def do_get_label(self):
        return self.abbr

    def do_get_info(self):
        if not self.info:
            return _('Info is not available')
        return gobject.markup_escape_text(self.info)


class PythonProvider(gobject.GObject, gsv.CompletionProvider):

    MARK_NAME = 'PythonProviderCompletionMark'

    def __init__(self, plugin):
        gobject.GObject.__init__(self)
        self.mark = None
        self._plugin = plugin

    def do_get_name(self):
        return _('Python')

    def do_get_activation(self):
        return gsv.COMPLETION_ACTIVATION_USER_REQUESTED

    def do_activate_proposal(self, proposal, textiter):
        # TODO: consider to use placeholder similar to snippet's magic
        buff = textiter.get_buffer()
        buff.begin_user_action()
        text = proposal.do_get_text()
        extratext = None
        if '(' in text:
            extratext = re.sub(r'.*\(', '', proposal.do_get_label())
            text += extratext
        buff.insert_at_cursor(text)

        start = buff.get_iter_at_mark(buff.get_insert())
        if extratext:
            while not start.get_char() == '(':
                start.backward_char()
            start.forward_char()
        buff.place_cursor(start)
        buff.end_user_action()
        return True

    def do_match(self, context):
        lang = context.get_iter().get_buffer().get_language()
        if lang.get_id() != 'python':
            return False
        return True

    def do_get_start_iter(self, context, proposal):
        buff = context.get_iter().get_buffer()
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            return None
        return buff.get_iter_at_mark(mark)

    def do_populate(self, context):
        textiter = context.get_iter()
        buff = textiter.get_buffer()
        if not textiter.ends_word or textiter.get_char() == '_':
            return

        start = textiter.copy()
        while not start.starts_line():
            start.backward_char()
            char = start.get_char()
            if not char.isalnum() and char not in "._":
                start.forward_char()
                break
        if start.equal(textiter):
            return

        contentfile = buff.get_text(*buff.get_bounds())
        match = textiter.get_text(start)
        line = textiter.get_line()

        if not contentfile:
            context.add_proposals(self, [], True)
            return

        self.move_mark(buff, start)
        proposals = self.get_proposals(contentfile, match, line)
        context.add_proposals(self, proposals, True)

    def get_proposals(self, contentfile, match, line):
        proposals = python_complete(contentfile, match, line)
        if not proposals:
            return []
        return [PythonProposal(proposal) for proposal in proposals]

    def move_mark(self, buff, start):
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            buff.create_mark(self.MARK_NAME, start, True)
        else:
            buff.move_mark(mark, start)


gobject.type_register(PythonProposal)
gobject.type_register(PythonProvider)
