import mailpile.app
import mailpile.commands
import mailpile.ui

# Load the standard plugins
from mailpile.plugins import *

__all__ = ['Mailpile',
           "app", "commands", "plugins", "mailutils", "search", "ui", "util"]


class Mailpile(object):
    """This object provides a simple Python API to Mailpile."""

    def __init__(self, ui=mailpile.ui.UserInteraction, workdir=None):
        self._config = mailpile.app.ConfigManager(workdir=workdir)
        self._session = mailpile.ui.Session(self._config)
        self._ui = self._session.ui = ui(self._config)
        self._session.config.load(self._session)
        self._session.main = True
        for cls in mailpile.commands.COMMANDS:
            names, argspec = cls.SYNOPSIS[1:3], cls.SYNOPSIS[3]
            if names[0]:
                setattr(self, *self._mk_action(cls, names[0], argspec))
            if names[1] and (names[0] != names[1]):
                setattr(self, *self._mk_action(cls, names[1], argspec))

    def _mk_action(self, cls, cmd, argspec):
        if argspec:

            def fnc(*args, **kwargs):
                return mailpile.commands.Action(self._session, cmd, args,
                                                data=kwargs)
        else:

            def fnc(**kwargs):
                return mailpile.commands.Action(self._session, cmd, '',
                                                data=kwargs)

        fnc.__doc__ = '%s(%s)  # %s' % (cmd, argspec or '', cls.__doc__)
        return cmd.replace('/', '_'), fnc

    def Interact(self):
        return mailpile.app.Interact(self._session)
