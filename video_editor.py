from moviepy.editor import*
import numpy as np
from image_editor import*
import os

cwd = os.getcwd()
def green_screen_replacement(green_screen_video, background_image_file, output_file):
    # Load your video
    clip = VideoFileClip(green_screen_video)
    clip_resized = clip.resize(height=1080 // 2)

    # Function to replace green screen with an image
    def replace_green_screen_with_image(image_array):
        green_screen_mask = np.full(image_array.shape, False)

        # Define color range for the green screen
        lower_green = np.array([200, 0, 0])
        upper_green = np.array([255, 50, 50])

        # Create a mask for the green screen
        green_screen_mask = ((image_array >= lower_green) & (image_array <= upper_green)).all(axis=2)

        # Load your background image
        background_image = VideoFileClip(background_image_file).get_frame(0)

        # Apply the mask to replace green screen with the background image
        image_array[green_screen_mask] = background_image[green_screen_mask]

        return image_array

    # Apply the function to each frame of the video
    new_clip = clip_resized.fl_image(replace_green_screen_with_image)

    # Write the result to a file
    new_clip.write_videofile(output_file, codec='libx264')

# Use the function
#green_screen_replacement("green_screen_video.mp4", "background.jpg","output_file.mp4")

def one_talking_heads_on_background(video_file1, background_image_file, output_file):
    # Load the videos
    video1 = VideoFileClip(video_file1)

    # Load the background image as a clip with the same duration as the videos
    background_clip = ImageClip(background_image_file, duration=video1.duration)

    # Resize the videos to fit in the corners and position them
    video1_resized = video1.resize(height=background_clip.h // 2) # adjust size as needed
    video1_resized.write_videofile(os.path.join(cwd, f'video\\temp\\left.mp4'), codec='libx264')
    left_img = os.path.join(cwd, 'video\\temp\\left.jpg')
    crop_image(background_image_file, 180, background_clip.h - video1_resized.h, 180 + video1_resized.w,
               background_clip.h, left_img)
    green_screen_replacement(os.path.join(cwd, f'video\\temp\\left.mp4'), left_img,
                             os.path.join(cwd, f'video\\temp\\left_p.mp4'))

    # Calculate the position of the videos at the bottom corners
    video1_position = (180, background_clip.h - video1_resized.h)

    # Position the videos
    video1_positioned = video1_resized.set_position(video1_position)

    # Combine everything
    final_clip = CompositeVideoClip([background_clip, video1_positioned])

    # Write the result to a file
    final_clip.write_videofile(output_file, codec='libx264')

# loop on vid2
def l2_two_talking_heads_on_background(video_file1, video_file2, background_image_file, output_file):
    # Load the videos
    video1 = VideoFileClip(video_file1)
    video2 = VideoFileClip(video_file2)

    # Ensure video2 is of the same duration as video1
    if video2.duration < video1.duration:
        num_loops = int(video1.duration) + 1
        looped_video2 = concatenate_videoclips([video2] * num_loops)
        looped_video2 = looped_video2.subclip(0, video1.duration)
    else:
        looped_video2 = video2.subclip(0, video1.duration)

    # Load the background image as a clip with the same duration as the videos
    background_clip = ImageClip(background_image_file, duration=looped_video2.duration)

    # Resize the videos to fit in the corners and position them
    video1_resized = video1.resize(height=background_clip.h // 2)# adjust size as needed
    video2_resized = looped_video2.resize(height=background_clip.h // 2)  # adjust size as needed
    video1_resized.write_videofile(os.path.join(cwd, f'video\\temp\\left.mp4'), codec='libx264')
    video2_resized.write_videofile(os.path.join(cwd, f'video\\temp\\right.mp4'), codec='libx264')

    # apply green screen to resized video
    left_img = os.path.join(cwd, 'video\\temp\\left.jpg')
    right_img = os.path.join(cwd, 'video\\temp\\right.jpg')
    crop_image(background_image_file, 180, background_clip.h - video1_resized.h, 180 + video1_resized.w,
               background_clip.h, left_img)
    crop_image(background_image_file, background_clip.w - video2_resized.w - 180, background_clip.h - video2_resized.h,
               background_clip.w - 180, background_clip.h, right_img)
    green_screen_replacement(os.path.join(cwd, f'video\\temp\\left.mp4'), left_img,
                             os.path.join(cwd, f'video\\temp\\left_p.mp4'))
    green_screen_replacement(os.path.join(cwd, f'video\\temp\\right.mp4'), right_img,
                             os.path.join(cwd, f'video\\temp\\right_p.mp4'))
    video1_resized = VideoFileClip(os.path.join(cwd, f'video\\temp\\left_p.mp4'))
    video2_resized = VideoFileClip(os.path.join(cwd, f'video\\temp\\right_p.mp4'))

    # Calculate the position of the videos at the bottom corners
    video1_position = (180, background_clip.h - video1_resized.h)
    video2_position = (background_clip.w - video2_resized.w - 180, background_clip.h - video2_resized.h)

    # Position the videos
    video1_positioned = video1_resized.set_position(video1_position)
    video2_positioned = video2_resized.set_position(video2_position)

    # Combine everything
    final_clip = CompositeVideoClip([background_clip, video1_positioned, video2_positioned])

    # Write the result to a file
    final_clip.write_videofile(output_file, codec='libx264')
# loop on vid1
def l1_two_talking_heads_on_background(video_file1, video_file2, background_image_file, output_file):
    # Load the videos
    video1 = VideoFileClip(video_file1)
    video2 = VideoFileClip(video_file2)

    # Ensure video2 is of the same duration as video1
    if video1.duration < video2.duration:
        num_loops = int(video2.duration)+1
        looped_video1 = concatenate_videoclips([video1] * num_loops)
        looped_video1 = looped_video1.subclip(0, video2.duration)
    else:
        looped_video1 = video1.subclip(0, video2.duration)

    # Load the background image as a clip with the same duration as the videos
    background_clip = ImageClip(background_image_file, duration=looped_video1.duration)

    # Resize the videos to fit in the corners and position them
    video1_resized = looped_video1.resize(height=background_clip.h // 2) # adjust size as needed
    video2_resized = video2.resize(height=background_clip.h // 2) # adjust size as needed
    video1_resized.write_videofile(os.path.join(cwd, f'video\\temp\\left.mp4'), codec='libx264')
    video2_resized.write_videofile(os.path.join(cwd, f'video\\temp\\right.mp4'), codec='libx264')

    # apply green screen to resized video
    left_img = os.path.join(cwd, 'video\\temp\\left.jpg')
    right_img = os.path.join(cwd, 'video\\temp\\right.jpg')
    crop_image(background_image_file, 180, background_clip.h - video1_resized.h, 180+video1_resized.w, background_clip.h, left_img)
    crop_image(background_image_file, background_clip.w - video2_resized.w-180, background_clip.h - video2_resized.h, background_clip.w-180, background_clip.h, right_img)
    green_screen_replacement(os.path.join(cwd, f'video\\temp\\left.mp4'), left_img, os.path.join(cwd, f'video\\temp\\left_p.mp4'))
    green_screen_replacement(os.path.join(cwd, f'video\\temp\\right.mp4'), right_img, os.path.join(cwd, f'video\\temp\\right_p.mp4'))
    video1_resized = VideoFileClip(os.path.join(cwd, f'video\\temp\\left_p.mp4'))
    video2_resized = VideoFileClip(os.path.join(cwd, f'video\\temp\\right_p.mp4'))

    # Calculate the position of the videos at the bottom corners
    video1_position = (180, background_clip.h - video1_resized.h)
    video2_position = (background_clip.w - video2_resized.w-180, background_clip.h - video2_resized.h)

    # Position the videos
    video1_positioned = video1_resized.set_position(video1_position)
    video2_positioned = video2_resized.set_position(video2_position)


    # Combine everything
    final_clip = CompositeVideoClip([background_clip, video1_positioned, video2_positioned])

    # Write the result to a file
    final_clip.write_videofile(output_file, codec='libx264')
def image_to_video(image_path, output_file, duration=10):
    # Load the image
    image_clip = ImageClip(image_path)

    # Set the duration of the video (in seconds)
    image_clip = image_clip.set_duration(duration)

    # Set the frames per second (fps) for the output video
    image_clip = image_clip.set_fps(fps=24)

    # Write the video to the specified output file
    image_clip.write_videofile(output_file, codec='libx264')
