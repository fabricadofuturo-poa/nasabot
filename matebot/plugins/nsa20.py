# vim:fileencoding=utf-8
#  Plugin nsa20 para matebot: NASA Space Apps Challenge
#  Copyleft (C) 2020 Iuri Guilherme, 2020 Fábrica do Futuro
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

import emojis, logging

from discord.ext.commands import Bot
from discord import utils

from matebot.plugins.nosql import redis_db

db = redis_db(db = 1)
## TODO: garantir que os cargos existem (testar a existência e criar se necessá\
## rio)
cargos = ['Desenvolvedor', 'Designer', 'Negócios', 'Cientista']
def check_desafios(desafios):
  pass
  ## FIXME voltar a ler o manual do Redis
  # ~ for desafio in range(1,22):
    # ~ try:
      # ~ db.set('desafio_' + str(desafio), desafios.get(str(desafio)))
    # ~ except Exception as exception:
      # ~ logging.warning(repr(exception))

async def change_role_callback(ctx):
  await ctx.message.author.add_roles(utils.get(ctx.message.guild.roles,
    name = str(ctx.command).capitalize()))
  for cargo in cargos:
    if str(ctx.command).capitalize() != cargo:
      await ctx.message.author.remove_roles(utils.get(ctx.message.guild.roles,
        name = cargo))
  logging.info(u"{0} mudou o cargo para {1}".format(ctx.author,
    str(ctx.command).capitalize()))

async def cadastrar_desafio_callback(ctx):
  pass

async def change_role_welcome_callback(*args):
  emoji = args[0]
  member = args[1]
  guild = args[2]
  if emoji == ':computer:':
    role = utils.get(guild.roles, name = 'Desenvolvedor')
  elif emoji == ':briefcase:':
    role = utils.get(guild.roles, name = 'Negócios')
  elif emoji == ':microscope:':
    role = utils.get(guild.roles, name = 'Cientista')
  elif emoji == ':art:':
    role = utils.get(guild.roles, name = 'Designer')
  else:
    role = None
  if role is not None and member is not None:
    await member.remove_roles(*[utils.get(guild.roles, name = cargo) \
      for cargo in cargos])
    await member.add_roles(role)
    logging.info(u"{0} mudou o cargo para {1}".format(member, role))

async def cadastrar_desafio_emoji_callback(*args):
  emoji = args[0]
  member = args[1]
  pass ## FIXME

def add_commands(bot: Bot):
  ## Popular o banco de dados com os dados da configuração
  ## FIXME pensar em formas que exigem menos interação manual para fazer isto
  check_desafios(bot.config_info['nsa20']['procuro_equipe']['desafios'])

  ## Altera cargo de acordo com comando
  @bot.command()
  async def dev(ctx):
    ctx.command = 'desenvolvedor'
    await change_role_callback(ctx)
  @bot.command()
  async def desenvolvedor(ctx):
    await change_role_callback(ctx)
  @bot.command()
  async def designer(ctx):
    await change_role_callback(ctx)
  @bot.command()
  async def negocios(ctx):
    ctx.command = 'negócios'
    await change_role_callback(ctx)
  @bot.command()
  async def cientista(ctx):
    await change_role_callback(ctx)

  @bot.event
  async def on_raw_reaction_add(payload):
    emoji = emojis.decode(str(payload.emoji)) or None
    message_id = payload.message_id
    guild = utils.find(lambda g : g.id == payload.guild_id, bot.guilds)
    channel = utils.find(lambda c : c.id == payload.channel_id, guild.channels)
    member = payload.member or None
    logging.info(u"{0} reagiu com {1} em {2} de {3}".format(
      member or '',
      emoji or '',
      channel or '',
      guild or '',
    ))
    ## Altera cargo de acordo com reação de emoji na mensagem de boas vindas
    if emoji is not None and message_id in [welcome['message'] for welcome in \
      bot.config_info['nsa20']['welcome']]:
      await change_role_welcome_callback(emoji,  member, guild)
    ## Cadastra intenção de participar de desafio através de emoji
    elif emoji is not None and message_id in [message for message in \
      bot.config_info['nsa20']['procuro_equipe']['messages']]:
      await cadastrar_desafio_emoji_callback(emoji, member)
  @bot.event
  async def on_raw_reaction_remove(payload):
    pass

  @bot.command()
  async def quero(ctx):
    cadastrar_desafio_callback(ctx)
