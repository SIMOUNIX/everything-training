import asyncio

from fastmcp import Client

client = Client("server.py")


async def main():
    async with client:
        # test create_note
        result = await client.call_tool(
            "create_note",
            {
                "title": "Test Note",
                "content": "This is my first real note.",
                "tags": ["test", "learning"],
            },
        )
        print(result)


asyncio.run(main())
