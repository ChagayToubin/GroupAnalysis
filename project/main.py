from project.manager import ManagerServer
import asyncio

async def main():
    manager = ManagerServer()
    await manager.app()

if __name__ == "__main__":
    asyncio.run(main())
