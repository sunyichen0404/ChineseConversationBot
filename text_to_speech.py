import edge_tts
import asyncio
import os

async def make_mp3(text, voice, output_file):
    if voice == 'male':
        communicate = edge_tts.Communicate(text, "zh-CN-YunjianNeural")
        await communicate.save(output_file)
    if voice == 'female':
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoyiNeural")
        await communicate.save(output_file)
    if voice == 'ai':
        communicate = edge_tts.Communicate(text, "zh-CN-YunyangNeural")
        await communicate.save(output_file)
def make_chinese_audio(text, voice,output_file):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_mp3(text, voice,output_file))
