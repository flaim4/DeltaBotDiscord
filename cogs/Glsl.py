import disnake
from disnake.ext import commands
from util._init_ import CogBase, Indelifer
import moderngl
import aiohttp
import diskcache
#ctx.author.avatar.url
ctx = moderngl.create_standalone_context()
width, height = 512, 256

avatar_cache = diskcache.Cache('./data/cache/avatars')


@Indelifer("glsl")
class Glsl(CogBase):
    async def init(self) -> None:
        with open('./data/shaders/vertex.glsl', 'r', encoding='utf-8') as f:
            vertex_shader = f.read()

        with open('./data/shaders/fragment.glsl', 'r', encoding='utf-8') as f:
            fragment_shader = f.read()

        self.prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        
        self.logger.info("Shader compiled successfully.")



    async def download_avatar(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    @commands.command()
    async def glsl(self, ctx: commands.Context):
        

