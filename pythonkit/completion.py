# -*- coding: utf-8 -*-
from gi.repository import GObject, GtkSource, GLib, Gio
import ConfigParser
import os
import re
import sys
from gettext import gettext as _
from parser import complete as python_complete


class PythonProposal(GObject.Object, GtkSource.CompletionProposal):

    def __init__(self, proposal):
        GObject.Object.__init__(self)
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
        return GLib.markup_escape_text(self.info)


class PythonProvider(GObject.Object, GtkSource.CompletionProvider):

    MARK_NAME = 'PythonProviderCompletionMark'

    DJANGOPROJECT_DIR = None

    DJANGOPROJECT_LOADED = False

    VIRTUALENV_DIR = None

    VIRTUALENV_LOADED = False

    def __init__(self, plugin):
        GObject.Object.__init__(self)
        self.mark = None
        self._plugin = plugin

    def do_get_name(self):
        return _('Python')

    def do_get_activation(self):
        return GtkSource.CompletionActivation.USER_REQUESTED

    def do_activate_proposal(self, proposal, textiter):
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
        if not lang or lang.get_id() != 'python':
            return False
        return True

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

        self.move_mark(buff, start)
        start_bound, end_bound = buff.get_bounds()

        contentfile = buff.get_text(start_bound, end_bound, False)
        match = textiter.get_text(start)
        line = textiter.get_line()

        self.load_configfile()
        self.load_virtualenv()
        self.load_django_settings()

        proposals = python_complete(contentfile, match, line)
        if not proposals:
            context.add_proposals(self, [], True)
        else:
            proposals = [PythonProposal(proposal) for proposal in proposals]
            context.add_proposals(self, proposals, True)

    def move_mark(self, buff, start):
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            buff.create_mark(self.MARK_NAME, start, True)
        else:
            buff.move_mark(mark, start)


    def load_django_settings(self):
        """
        Force django to load its settings for the first time.
        """
        if self.DJANGOPROJECT_LOADED is True:
            return

        if not self.DJANGOPROJECT_DIR:
            return

        if os.path.exists(os.path.join(self.DJANGOPROJECT_DIR, 'settings.py')):
            try:
                sys.path.append(self.DJANGOPROJECT_DIR)
                from django.core.management import setup_environ
                import settings
                setup_environ(settings)
                self.DJANGOPROJECT_LOADED = True
            except:
                pass

    def load_virtualenv(self):
        if self.VIRTUALENV_LOADED is True:
            return

        if not self.VIRTUALENV_DIR:
            return

        if os.path.exists(self.VIRTUALENV_DIR):
            if sys.platform == 'win32':
                exec_path = os.path.join(self.VIRTUALENV_DIR, 'scripts')
            else:
                exec_path = os.path.join(self.VIRTUALENV_DIR, 'bin')

            exec_path = os.path.join(exec_path, 'activate_this.py')
            if os.path.exists(exec_path) and os.path.isfile(exec_path):
                execfile(exec_path, dict(__file__=exec_path))
                self.VIRTUALENV_LOADED = True

    def filebrowser_root(self):
        """ Get path to current filebrowser root. """
        settings = Gio.Settings.new('org.gnome.gedit.plugins.filebrowser')
        virtual_root = settings.get_string('virtual-root').split('file://')[1]
        return virtual_root

    def load_configfile(self):
        conf_file = os.path.join(self.filebrowser_root(), '.pythonkit')
        config_parser = ConfigParser.SafeConfigParser()
        config_parser.read(conf_file)
        try:
            self.DJANGOPROJECT_DIR = config_parser.get('pythonkit',
                'djangoproject_dir')
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass

        try:
            self.VIRTUALENV_DIR = config_parser.get('pythonkit',
                'virtualenv_dir')
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass


GObject.type_fundamental(PythonProposal)
GObject.type_fundamental(PythonProvider)
