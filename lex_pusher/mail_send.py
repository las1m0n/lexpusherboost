# -*- coding: utf-8 -*-
# coding: utf-8
from __future__ import unicode_literals

from mailer import Mailer
from mailer import Message


def send(to, key):
    message = Message(From="bondarenkonikita295@gmail.com",
                      To=to)
    message.Subject = "Flex Pusher Authentication"
    message.Html = f"""<div><div class="adM">
                        </div><p>Здравствуйте!</p>
                                <p>В системе FlexPusher только что был создан личный кабинет клиента для Вашего 
                                буста и в качестве адреса электронной почты был указан этот адрес электронной 
                                почты.<br> 
                                Если Вы не уверены, что это были Вы, то просто проигнорируйте это письмо.
                                </p>
                                <p>Для входа в <a href="/">
                                свой Личный кабинет</a>,
                                 пожалуйста, используйте следующие параметры:</p>
                                 <ul>
                                    <li>PIN: {key}
                                    </li>
                                </ul>
                                <div class="yj6qo"></div><div class="adL">
                                 </div></div>"""

    sender = Mailer('smtp.gmail.com', pwd="", usr="", use_tls=True)
    sender.send(message)
