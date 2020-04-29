import os
import json
import ulid
import asyncio
import traceback
import discord
from discord.ext import commands
from logging import getLogger, StreamHandler, DEBUG
from libs import *


formatter = JsonFormatter('{"timestamp": "%(asctime)-15s", "transaction-id": ' + f'"{ulid.new().str}"' + ', "level": "%(levelname)s", "message": %(message)s}')
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


description = '''マインクラフトサーバを起動する
'''


instance = os.environ['TARGET']
dns_zone = os.environ['ZONE']
dns_name = os.environ['NAME']
project = os.environ['PROJECT']
gcp_zone = os.environ['GCP_ZONE']
dns_ttl = os.environ['TTL']
dns_domain = os.environ['DOMAIN']
dns_auth_email = os.environ['AUTH_EMAIL']
dns_auth_key = os.environ['AUTH_KEY']
dns_zone_id = os.environ['ZONE_ID']
token = os.environ['DISCORD_TOKEN']


bot = commands.Bot(command_prefix='/', description=description)


@bot.event
async def on_ready():
    update_transaction_id(handler)

    # logger.debug({'env': json.dumps(os.environ)})
    logger.debug({'GOOGLE_APPLICATION_CREDENTIALS': os.environ['GOOGLE_APPLICATION_CREDENTIALS']})
    logger.debug({'TARGET': instance})
    logger.debug({'ZONE': dns_zone})
    logger.debug({'NAME': dns_name})
    logger.debug({'DOMAIN': dns_domain})
    logger.debug({'AUTH_EMAIL': dns_auth_email})
    logger.debug({'AUTH_KEY': anonymization(dns_auth_key)})
    logger.debug({'ZONE_ID': dns_zone_id})
    logger.debug({'TOKEN': anonymization(token)})

    logger.info('Logged in as')
    logger.info(bot.user.name)
    logger.info(bot.user.id)
    logger.info('------')


@bot.command(description='マイクラサーバの起動')
async def mcstart(ctx):
    transaction_id = ulid.new().str
    update_transaction_id(handler, transaction_id)
    logger.info(f'start transaction {transaction_id}')

    logger.info('call mcstart')
    await ctx.send('起動する')
    standup = Standup(logger)

    try:
        logger.info('start minecraft server...')
        res = standup.start_instance(project, gcp_zone, instance)
        logger.info('done starting minecraft server. ')
    except Exception as e:
        logger.warning(f'{e}')
        await ctx.send('失敗した')

    logger.info('get instance external ip...')
    ip = standup.get_instance_external_ip_address(project, gcp_zone, instance)
    logger.info(f'done getting instance external ip {ip}')

    logger.info('register dns...')
    res = standup.add_dns_record(dns_auth_email, dns_zone_id, dns_auth_key, dns_name, ip)
    logger.info('done registering dns. ')

    if res:
        await ctx.send(f'起動した 接続先-> {dns_name}')
    else:
        await ctx.send(f'起動してた 接続先-> {dns_name}')

    logger.info(f'end transaction {transaction_id}')


@bot.command(description='マイクラサーバの停止')
async def mcstop(ctx):
    transaction_id = ulid.new().str
    update_transaction_id(handler, transaction_id)
    logger.info(f'start transaction {transaction_id}')

    logger.info('call mcstop')
    await ctx.send('停止する')
    shutdown = Shutdown(logger)

    try:
        logger.info('stop minecraft server...')
        res = shutdown.stop_instance(project, gcp_zone, instance)
        logger.info('done stopping minecraft server. ')
    except Exception as e:
        logger.warning(f'{e}')
        await ctx.send('失敗した')
        exit(1)

    try:
        logger.info('unregister dns...')
        res = shutdown.delete_dns_record(dns_auth_email, dns_zone_id, dns_auth_key, dns_name)
        logger.info('done unregistering dns. ')
    except IndexError as e:
        logger.warning(f'{e}')
        # await ctx.send('停止してた')

    await ctx.send('停止した')
    logger.info(f'end transaction {transaction_id}')


bot.run(token)

