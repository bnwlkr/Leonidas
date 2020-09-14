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

        mock_guild.return_value.channels = []
        test_course = course.Course('CPSC', '110', '101')
        
        channels = ['cpsc', 'cpsc-110', 'cpsc-110-101']
        i = 0
        async for _ in server.create_channels(mock_guild, mock_subjs_category, test_course):
            if i == 0:
                mock_subjs_category.create_text_channel.\
                        assert_called_once_with(channels[i],
                                                overwrites=secret)
                continue
            create_channel_mock = mock_guild.create_category.return_value.create_text_channel
            create_channel_mock.assert_called_with(channels[i], overwrites=secret)
            i += 1

        mock_guild.create_category.assert_called_once_with('cpsc-110', overwrites=secret)
        
