import asyncio
import aiounittest
from unittest import mock

import discord

from leonidas import course, server

class TestServer(aiounittest.AsyncTestCase):
    async def test_create_channels_course(self):
        mock_guild = mock.AsyncMock(discord.Guild)
        test_course = course.Course('CPSC', '110', '101')
        async for _ in server.create_channels(mock_guild, test_course):
            pass
        mock_guild.create_category.assert_called_once()
