from Skype4Py import skype
from Skype4Py.enums import cmsReceived, chatTypeDialog, chatTypeLegacyDialog

from bender.decorators import backbone_start, backbone_shutdown


class BenderSkype(object):

    def __init__(self):
        self.on_message_received = None
        self._skype = None

    @backbone_start
    def start(self):
        self._skype = _skype = skype.Skype()
        _skype.RegisterEventHandler(
            'MessageStatus',
            self._on_message_status,
        )
        _skype.RegisterEventHandler(
            'UserAuthorizationRequestReceived',
            self._on_authorization_request,
        )
        _skype.Attach()

        for user in _skype.UsersWaitingAuthorization:
            self._on_authorization_request(user)

        print('Connected to %s account.' % _skype.CurrentUserHandle)

    @backbone_shutdown
    def shutdown(self):
        del self._skype

    def _on_message_status(self, msg, status):
        '''
        Invoked whenever :meth:`Skype4Py.skype.SkypeEvents.MessageStatus`
        is triggered.

        Only received messages will be handled by :class:`Bot`.

        .. seealso:: :class:`Skype4Py.utils.EventHandlingBase`
        '''
        # Handling only received messages.
        if status != cmsReceived:
            return

        # Handling only 1-to-1 dialogs.
        if msg.Chat.Type not in (chatTypeDialog, chatTypeLegacyDialog):
            return

        msg.MarkAsSeen()
        msg = SkypeMessage(msg)
        self.on_message_received(msg)

    def _on_authorization_request(self, user):
        '''
        Invoked whenever
        :meth:`Skype4Py.skype.SkypeEvents.UserAuthorizationRequestReceived`
        is triggered.

        Automatically accept friend request.

        .. seealso:: :class:`Skype4Py.utils.EventHandlingBase`
        '''
        user.IsAuthorized = True


class SkypeMessage(object):

    def __init__(self, msg):
        if isinstance(msg, int):
            _skype = skype.Skype()
            msg = _skype.Message(msg)
        self._msg = msg

    def get_body(self):
        return self._msg.Body

    def reply(self, message):
        self._msg.Chat.SendMessage(message)

    def get_sender(self):
        return self._msg.FromHandle

    def __reduce__(self):
        return (self.__class__, (self._msg.Id,))
