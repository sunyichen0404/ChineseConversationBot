from text_abstractor import *
from image_editor import *
from video_editor import *
from text_to_speech import *
import subprocess
import os

cwd = os.path.dirname(os.path.abspath(__file__))
clips = []
crossfade_duration = 0.5

i = 0
t_counter = 0
s_counter = 0
ai_counter = 0

for t in text.split('\n'):
    print(t, i)

    if t.startswith("【场景"):
        bkg = t.split('：')[1]
        bkg_image = os.path.join(cwd, f"img\\bkg\\{bkg}.jpg")
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')
        image_to_video(bkg_image, output_video_path, duration=2.5)

        clip = VideoFileClip(output_video_path)
        clip = clip.crossfadein(crossfade_duration).crossfadeout(crossfade_duration)
        clips.append(clip)
        i += 1

    # title card
    if t.startswith('['):
        chinese = t
        background_image_path = os.path.join(cwd, 'img\\bkg\\blackboard.jpg')
        output_image_path = os.path.join(cwd, f'img\\title_card\\{title}.jpg')
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')

        create_title_card(chinese, background_image_path, output_image_path)
        image_to_video(output_image_path, output_video_path, duration=2.5)

        clip = VideoFileClip(output_video_path)
        clip = clip.crossfadeout(crossfade_duration)
        clips.append(clip)
        i += 1

    # student teacher talking head
    if t.startswith("T："):
        # making audio file
        text_value = t[2:]
        output_audio_file = os.path.join(cwd, f"audio\\T_{t_counter}.mp3")
        #make_chinese_audio(text_value, output_audio_file, False)

        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\t.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\T_{t_counter}')
        #command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess crop --enhancer gfpgan"
        #subprocess.run(command, shell=True)

        # making talking head video
        video1 = os.path.join(cwd, f'video\\LipSycned\\S_D.mp4')
        video2 = os.path.join(cwd, f'video\\LipSycned\\T_{t_counter}',
                              os.listdir(os.path.join(cwd, f'video\\LipSycned\\T_{t_counter}'))[0])
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')
        l1_two_talking_heads_on_background(video1, video2, bkg_image, output_video_path)

        clip = VideoFileClip(output_video_path)
        clips.append(clip)
        i += 1
        t_counter += 1

    # student teacher talking head
    if t.startswith("S：") and 'To AI' not in t:
        # making audio file
        text_value = t[2:]
        output_audio_file = os.path.join(cwd, f"audio\\S_{s_counter}.mp3")
        make_chinese_audio(text_value, output_audio_file, False)
        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\s.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}')
        #command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess crop --enhancer gfpgan"
        #subprocess.run(command, shell=True)
        # making talking head video
        video1 = os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}',
                              os.listdir(os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}'))[0])
        video2 = os.path.join(cwd, f'video\\LipSycned\\T_D.mp4')
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')

        l2_two_talking_heads_on_background(video1, video2, bkg_image, output_video_path)

        clip = VideoFileClip(output_video_path)
        clips.append(clip)
        i += 1
        s_counter += 1

    #ai student talking head
    if t.startswith("S：") and 'To AI' in t:
        # making audio file
        text_value = t[8:]
        output_audio_file = os.path.join(cwd, f"audio\\S_{s_counter}.mp3")
        make_chinese_audio(text_value, output_audio_file, False)
        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\s.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}')
        #command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess crop --enhancer gfpgan"
        #subprocess.run(command, shell=True)
        # making talking head video
        video1 = os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}',
                              os.listdir(os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}'))[0])
        video2 = os.path.join(cwd, f'video\\LipSycned\\A_D.mp4')
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')
        l2_two_talking_heads_on_background(video1, video2, bkg_image, output_video_path)

        clip = VideoFileClip(output_video_path)
        clips.append(clip)
        i += 1
        s_counter += 1

    # ai talking head
    if t.startswith("AI：") and 'AI appears' in t:
        # making audio file
        text_value = t[15:]
        output_audio_file = os.path.join(cwd, f"audio\\AI_{ai_counter}.mp3")
        make_chinese_audio(text_value, output_audio_file, False)
        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\ai.jpg')
        #result_dir = os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}')
        #command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess crop --enhancer gfpgan"
        #subprocess.run(command, shell=True)
        # one talking head on background
        video1 = os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}',
                              os.listdir(os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}'))[0])
        background_image_file = os.path.join(cwd, 'img\\bkg\\aispace.jpg')
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}_before&after.mp4')
        one_talking_heads_on_background(video1, background_image_file, output_video_path)

        clip = VideoFileClip(output_video_path)
        clip = clip.crossfadein(crossfade_duration).crossfadeout(crossfade_duration)
        clips.append(clip)
        i += 1
        ai_counter += 1

    # ai student talking head
    if t.startswith("AI：") and 'AI appears' not in t:
        # making audio file
        text_value = t[2:]
        output_audio_file = os.path.join(cwd, f"audio\\AI_{ai_counter}.mp3")
        make_chinese_audio(text_value, output_audio_file, False)
        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\ai.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}')
        #command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess crop --enhancer gfpgan"
        #subprocess.run(command, shell=True)
        # making talking head video
        video1 = os.path.join(cwd, f'video\\LipSycned\\S_D.mp4')
        video2 = os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}',
                              os.listdir(os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}'))[0])
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')
        l1_two_talking_heads_on_background(video1, video2, bkg_image, output_video_path)

        clip = VideoFileClip(output_video_path)
        clips.append(clip)
        i += 1
        ai_counter += 1

# Concatenate clips with transitions
final_clip = concatenate_videoclips(clips)

# Write the result to a file
output_video_path = os.path.join(cwd, f'video\\output\\{title}.mp4')
final_clip.write_videofile(output_video_path)
