import asyncio
import aiounittest
from unittest import mock

import discord

from leonidas import course, server


class TestServer(aiounittest.AsyncTestCase):
    async def test_create_channels_course(self):
        pass  # TODO
      #  mock_guild = mock.AsyncMock(discord.Guild)
      #  test_course = course.Course('CPSC', 110)
      #  mock_guild.create_category.return_value = 'CPSC'
      #  await server.create_channels(mock_guild, test_course)
      #  mock_guild.create_category.assert_called_once_with('CPSC')
      #  mock_guild.create_text_channel.assert_called_once_with('cpsc-110', 'CPSC')
