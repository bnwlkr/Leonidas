import asyncio
import aiounittest
from unittest import mock

import discord

from leonidas import course, server

class TestServer(aiounittest.AsyncTestCase):
    async def test_create_channels_course(self):
        mock_guild = mock.AsyncMock(discord.Guild)
        mock_subjs_category = mock.AsyncMock(discord.CategoryChannel)

        secret = {
            mock_guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        test_course = course.Course('CPSC', '110')
        
        await server.create_channels(mock_guild, test_course)

        mock_guild.create_text_channel.assert_called_with('cpsc-110', overwrites=secret)

