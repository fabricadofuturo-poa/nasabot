# vim:fileencoding=utf-8
#  Plugin feedback para matebot: Envia feedback para o grupo de administração.
#  Copyleft (C) 2016-2020 Iuri Guilherme, 2017-2020 Matehackers,
#    2018-2019 Velivery, 2019 Greatful, 2019-2020 Fábrica do Futuro
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  

## TODO: Este plugin nunca foi testado para a eventualidade da inexistência ou não permissão de envio para o grupo de administração.
## TODO: try sem finally
def cmd_feedback(args):
  try:
    if len(args['command_list']) > 0:
      return {
        'status': True,
        'type': "feedback",
        'response': u"Obrigado pelo feedback! Alguém em algum momento vai ler, eu acho.",
        'feedback': ' '.join(args['command_list']),
        'debug': u'Feedback bem sucedido',
        'multi': False,
        'parse_mode': None,
        'reply_to_message_id': args['message_id'],
      }
    else:
      response = u"Erro tentando enviar feedback. Você deve seguir este modelo:\n\n/feedback Digite a mensagem aqui"
      debug = u"Feedback falhou, mensagem vazia"
  except Exception as e:
    response = u"Erro tentando enviar feedback. Os desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Feedback falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': "erro",
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

def cmd_f(args):
  return cmd_feedback(args)

## Aiogram
def add_handlers(dispatcher):
  from matebot.aio_matebot.controllers.callbacks import command_callback
  from aiogram import exceptions
  @dispatcher.message_handler(
    commands = ['feedback', 'f'],
  )
  async def feedback_callback(message):
    await command_callback(message, 'feedback')
    try:
      await dispatcher.bot.send_message(
        chat_id = dispatcher.bot.users['special']['feedback'],
        text = u"""\#feedback enviado de {first_name} {last_name} 
\({username}\):\n`{feedback}`""".format(
          first_name = message.from_user.first_name,
          last_name = message.from_user.last_name,
          username = message.from_user.id,
          feedback = message.get_args(),
        ),
        parse_mode = "MarkdownV2",
      )
      await message.reply(u"""Obrigado pelo feedback! Alguém em algum momento \
vai ler, eu acho...""")
    except exceptions.MessageTextIsEmpty:
      await message.reply(u"""Obrigado pela tentativa, mas se for pra mandar \
feedback tem que escrever alguma coisa\! Exemplo:\n\
`{} Muito obrigado pelo bot!`""".format(message.get_command()),
        parse_mode = "MarkdownV2",
      )
