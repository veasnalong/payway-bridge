import os, asyncio, logging, aiohttp
from telethon import TelegramClient, events

API_ID       = int(os.environ.get('BRIDGE_API_ID', '0'))
API_HASH     = os.environ.get('BRIDGE_API_HASH', 'YOUR_API_HASH')
PHONE        = os.environ.get('BRIDGE_PHONE', '+1xxxxxxxxxx')
BOT_URL      = os.environ.get('BOT_URL', 'http://localhost:8080')
SECRET       = os.environ.get('BRIDGE_SECRET', 'changeme')

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('bridge_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def on_msg(event):
    text = event.raw_text or ''
    if not text: return
    # Only forward PayWay messages
    if 'paid by' not in text.lower() and 'trx. id' not in text.lower(): return
    logger.info('PayWay msg detected in chat %s - forwarding...', event.chat_id)
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                BOT_URL+'/webhook',
                json={'text': text, 'chat_id': event.chat_id, 'secret': SECRET},
                timeout=aiohttp.ClientTimeout(total=10)
            )
        logger.info('Forwarded to bot OK')
    except Exception as e:
        logger.error('Forward failed: %s', e)

async def main():
    await client.start(phone=PHONE)
    me = await client.get_me()
    logger.info('Bridge running as: %s', me.first_name)
    logger.info('Watching ALL groups for PayWay messages...')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
