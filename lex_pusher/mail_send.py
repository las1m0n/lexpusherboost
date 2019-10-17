# -*- coding: utf-8 -*-
# coding: utf-8
from __future__ import unicode_literals

from mailer import Mailer
from mailer import Message


def send(to, key):
    message = Message(From="lexpusher77@gmail.com",
                      To=to, charset="utf-8")
    message.Subject = "Lex Pusher Authentication"
    message.Html = f"""<div><div class="adM">
                        </div><p>Здравствуйте!</p>
                                <p>В системе LexPusher только что был создан личный кабинет клиента для Вашего 
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

<<<<<<< HEAD
    sender = Mailer('smtp.gmail.com', pwd="5525458565", usr="lexpusher77@gmail.com", use_tls=True)
=======
    sender = Mailer('smtp.gmail.com', pwd="", usr="bondarenkonikita295@gmail.com", use_tls=True)
>>>>>>> 83918972b4662bcc65278f3da4e45aaa5ffa97d1
    sender.send(message)


def send_payout(to, nickname, id):
    message = Message(From="lexpusher77@gmail.com",
                      To=to, charset="utf-8")
    message.Subject = "Lex Pusher"
    message.Html = f"""<div><div class="adM">
                        </div><p>Здравствуйте!</p>
                        <p>Поступил запрос на выплату</p>
                                 <ul>
                                    <li>Имя бустера: {nickname} (id={id})
                                    </li>
                                </ul>
                                <div class="yj6qo"></div><div class="adL">
                                 </div></div>"""

<<<<<<< HEAD
    sender = Mailer('smtp.gmail.com', pwd="5525458565", usr="lexpusher77@gmail.com", use_tls=True)
=======
    sender = Mailer('smtp.gmail.com', pwd="", usr="bondarenkonikita295@gmail.com", use_tls=True)
>>>>>>> 83918972b4662bcc65278f3da4e45aaa5ffa97d1
    sender.send(message)


def send_data_account(to, st_login, st_pass, em_login, em_pass):
    message = Message(From="lexpusher77@gmail.com",
                      To=to, charset="utf-8")
    message.Subject = "Lex Pusher"
    message.Html = f"""<div><div class="adM">
                        </div><p>Здравствуйте!</p>
                                <p>Поздравляем с покупкой аккаунта.<br> 
                                Если Вы не уверены, что это были Вы, то просто проигнорируйте это письмо.
                                </p>
                                 <ul>
                                    <li>Логин Steam: {st_login}
                                    </li>
                                    <li>Пароль от аккаунта: {st_pass}
                                    </li>
                                    <li>Email: {em_login}
                                    </li>
                                    <li>Пароль от почты: {em_pass}
                                    </li>
                                </ul>
                                <div class="yj6qo"></div><div class="adL">
                                 </div></div>"""

<<<<<<< HEAD
    sender = Mailer('smtp.gmail.com', pwd="5525458565", usr="lexpusher77@gmail.com", use_tls=True)
    sender.send(message)
=======
    sender = Mailer('smtp.gmail.com', pwd="", usr="bondarenkonikita295@gmail.com", use_tls=True)
    sender.send(message)
>>>>>>> 83918972b4662bcc65278f3da4e45aaa5ffa97d1
