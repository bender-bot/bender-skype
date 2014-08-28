from Skype4Py import skype  # @UnusedImport # noqa
from Skype4Py.enums import cmsReceived, chatTypeDialog
from mock import patch, call, MagicMock, ANY

import bender_skype


@patch('Skype4Py.skype.Skype', autospec=True)
def test_bender_skype(mock_Skype):

    chat_message = MagicMock()
    on_message_received = MagicMock()
    user = MagicMock()

    bb = bender_skype.BenderSkype()
    bb.on_message_received = on_message_received
    mock_Skype.return_value.UsersWaitingAuthorization = [user]
    assert bb._skype is None

    bb.start()
    assert bb._skype is not None
    mock_Skype.assert_called_once_with()
    assert mock_Skype.return_value.RegisterEventHandler.mock_calls == [
        call('MessageStatus', bb._on_message_status),
        call('UserAuthorizationRequestReceived', bb._on_authorization_request),
    ]
    mock_Skype.return_value.Attach.assert_called_once_with()
    assert user.IsAuthorized is True

    bb._on_message_status(None, None)
    assert on_message_received.called is False

    bb._on_message_status(chat_message, cmsReceived)
    assert on_message_received.called is False

    chat_message.Chat.Type = chatTypeDialog
    chat_message.Body = 'This is my sexy body!'
    chat_message.FromDisplayName = 'foo'

    bb._on_message_status(chat_message, cmsReceived)
    on_message_received.assert_called_once_with(ANY)

    received_message = on_message_received.call_args[0][0]
    assert received_message.get_body() == 'This is my sexy body!'
    assert received_message.get_sender() == 'foo'

    received_message.reply('Yey!')
    chat_message.Chat.SendMessage.assert_called_once_with('Yey!')
