from text_abstractor import *
from video_editor import *
from text_to_speech import *
import subprocess
import os

cwd = os.getcwd()
clips = []
crossfade_duration = 0.2

i = 0
t_counter = 0
s_counter = 0
ai_counter = 0


def find_mp4_file(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out the .mp4 file
    mp4_files = [f for f in files if f.endswith('.mp4')]

    # Return the first .mp4 file found, or None if no .mp4 file is found
    return mp4_files[0] if mp4_files else None

for t in text.split('\n'):
    print(i,'|',t)

    if t.startswith("【场景"):
        bkg = t.split('：')[1]
        bkg_image = os.path.join(cwd, f"img\\bkg\\{bkg}.jpg")
        output_video_path = os.path.join(cwd, f'video\\temp\\{i}.mp4')
        image_to_video(bkg_image, output_video_path, duration=2.5)

        clip = VideoFileClip(output_video_path)
        clip = clip.crossfadein(crossfade_duration).crossfadeout(crossfade_duration)
        clips.append(clip)
        i += 1

    if t.startswith('Prop:'):
        text_value = t[5:]
        make_prop(text_value, os.path.join(cwd, f'img\\prop\\{text_value}.jpg'), bkg_image)
        bkg_image = os.path.join(cwd, f'img\\prop\\{text_value}.jpg')
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
        make_chinese_audio(text_value, 'female', output_audio_file)

        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\t.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\T_{t_counter}')
        command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess full --enhancer gfpgan"
        subprocess.run(command, shell=True)

        # making talking head video
        vid = find_mp4_file(os.path.join(cwd, f'video\\LipSycned\\T_{t_counter}'))
        video1 = os.path.join(cwd, f'video\\LipSycned\\S_D.mp4')
        video2 = os.path.join(cwd, f'video\\LipSycned\\T_{t_counter}',vid)
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
        make_chinese_audio(text_value, 'male', output_audio_file)
        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\s.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}')
        command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess full --enhancer gfpgan"
        subprocess.run(command, shell=True)
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
        make_chinese_audio(text_value, 'male', output_audio_file)
        # sadtalker run
        driven_audio = output_audio_file
        source_image = os.path.join(cwd, 'img\\character\\s.jpg')
        result_dir = os.path.join(cwd, f'video\\LipSycned\\S_{s_counter}')
        command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess full --enhancer gfpgan"
        subprocess.run(command, shell=True)
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
        make_chinese_audio(text_value, 'ai', output_audio_file)
        # make ai img into video
        image_clip = ImageClip(os.path.join(cwd, 'img\\character\\ai.jpg'))
        audio = AudioFileClip(output_audio_file)
        image_clip = image_clip.set_duration(audio.duration)
        image_clip.write_videofile(os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}.mp4'), fps=24)

        # one talking head on background
        video1 = os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}.mp4')
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
        make_chinese_audio(text_value, 'ai', output_audio_file)
        # make ai img into video
        image_clip = ImageClip(os.path.join(cwd, 'img\\character\\ai.jpg'))
        audio = AudioFileClip(output_audio_file)
        image_clip = image_clip.set_duration(audio.duration)
        image_clip.write_videofile(os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}.mp4'), fps=24)

        # making talking head video
        video1 = os.path.join(cwd, f'video\\LipSycned\\S_D.mp4')
        video2 = os.path.join(cwd, f'video\\LipSycned\\AI_{ai_counter}.mp4')
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
