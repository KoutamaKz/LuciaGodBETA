import asyncio
from utils.core import client, loadCogs, configData

if __name__ == '__main__':
    async def main():
        async with client:
            await loadCogs()
            await client.start(configData['TOKEN'])
        
    asyncio.run(main())