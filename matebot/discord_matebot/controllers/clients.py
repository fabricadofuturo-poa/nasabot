# -*- coding: utf-8 -*-
#
#  Matebot
#  
#  Copyleft 2012-2020 Iuri Guilherme <https://github.com/iuriguilherme>,
#     Matehackers <https://github.com/matehackers>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import json, logging, sys

from discord import (
  Client,
  errors,
)
from discord.ext.commands import Bot
from matebot.discord_matebot.controllers.events import add_events

class MateClient(Client):
  def __init__(self, *args, **kwargs):
    ## Tratando as configurações
    config = kwargs.get('config')
    name = kwargs.get('name', 'matebot')
    setattr(self, 'config_info',
      config.bots[name]['info'] or config.default_bot['info'])
    setattr(self, 'config_plugins',
      config.bots[name]['plugins'] or config.default_bot['plugins'])
    setattr(self, 'config_users',
      config.bots[name]['users'] or config.default_bot['users'])
    kwargs.pop('config', None)
    kwargs.pop('name', None)
    super().__init__(*args, **kwargs)
    add_events(self)

  # ~ async def on_message(*args, **kwargs):
    # ~ logging.info(u"""Mensagem de {author} no canal #{channel} do servidor {guil\
# ~ d}: {content}""".format(
        # ~ author = args[1].author or '',
        # ~ channel = args[1].channel or '',
        # ~ guild = args[1].guild or '',
        # ~ content = args[1].content or '',
      # ~ )
    # ~ )

  ## Mensagens apagadas
  ## Ver também:
  ## on_bulk_message_delete
  ## on_raw_message_delete
  ## on_raw_bulk_message_delete
  # ~ async def on_message_delete(message):
    # ~ logging.info(u"Mesagem apagada: {}".format(message))

  ## Mensagem atualizada
  # ~ async def on_message_edit(before, after):
    # ~ logging.info(u"Mesagem atualizada. Era: {0}\n\nAgora: {1}".format(
      # ~ before, after))

  ## Reações
  # ~ async def on_reaction_add(reaction, user):
    # ~ logging.info(u"Reação de {0} em {1}:\n\n{2}".format(
      # ~ user, reaction.message, reaction))
  # ~ async def on_reaction_remove(reaction, user):
    # ~ logging.info(u"Reação removida de {0} em {1}:\n\n{2}".format(
      # ~ user, reaction.message, reaction))

  ## Servidores
  # ~ async def on_guild_join(guild):
    # ~ logging.info(u"Entramos no servidor {}".format(guild))
  # ~ async def on_guild_remove(guild):
    # ~ logging.info(u"Saímos do servidor {}".format(guild))

  ## Usuários
  # ~ async def on_member_join(member):
    # ~ logging.info(u"{} entrou no servidor".format(member))
  # ~ async def on_member_remove(member):
    # ~ logging.info(u"{} saiu do servidor".format(member))

  ## Tratamento de erros
  async def on_error(event, *args, **kwargs):
    logging.warning(
      u"event: {0}\n\nargs: {1}\n\nkwargs: {2}\n\nexception: {3}".format(
        str(event),
        str(args),
        str(kwargs),
        str(sys.exc_info()),
      )
    )
    await super().on_error(event, *args, **kwargs)

class MateBot(Bot):
  def __init__(self, *args, **kwargs):
    ## Tratando as configurações
    config = kwargs.get('config')
    name = kwargs.get('name', 'matebot')
    setattr(self, 'config_info',
      config.bots[name]['info'] or config.default_bot['info'])
    setattr(self, 'config_plugins',
      config.bots[name]['plugins'] or config.default_bot['plugins'])
    setattr(self, 'config_users',
      config.bots[name]['users'] or config.default_bot['users'])
    kwargs.pop('config', None)
    kwargs.pop('name', None)
    super().__init__(*args, **kwargs)
    add_events(self)

  async def on_message(self, *args, **kwargs):
    logging.info(u"""Mensagem de {author} no canal #{channel} do servidor {guil\
d}: {content}""".format(
        author = args[0].author or '',
        channel = args[0].channel or '',
        guild = args[0].guild or '',
        content = args[0].content or '',
      )
    )

  # ~ async def on_member_join(self, *args, **kwargs):
    # ~ logging.info(u"{} entrou no servidor".format(args[0]))

  async def on_ready(self):
    logging.info(u"""Conectada com sucesso, o nosso nome de usuário é {0.user}\
""".format(self))

  async def on_error(event, *args, **kwargs):
    logging.warning(
      u"event: {0}\n\nargs: {1}\n\nkwargs: {2}\n\nexception: {3}".format(
        str(event),
        str(args),
        str(kwargs),
        str(sys.exc_info()),
      )
    )
    await super().on_error(event, *args, **kwargs)


