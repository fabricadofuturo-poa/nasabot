# vim:fileencoding=utf-8

def default(info_dict, bot_dict, addr_dict, command_list):
  raise AttributeError

def teste(info_dict, bot_dict, addr_dict, command_list):
  response = u'Deu certo!'
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'teste',
  }

