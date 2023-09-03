import time
import random
from flask import Flask, request, jsonify
from moviepy.editor import *

app = Flask(__name__)


@app.route('/', methods=['POST'])
def run():
    try:
        data = request.json
        URL = data.get('URL')
        overlay = data.get('overlay')
        title = data.get('title')  # Get the title from JSON

        if URL is not None and overlay is not None:

            print('Load the video clip')
            # Load the video clip
            clip = VideoFileClip(URL)

            print('Adding overlay image')
            # Load the overlay image
            overlay_image = ImageClip(overlay)

            # Create overlay with the same duration as the clip
            overlay_clip = overlay_image.set_duration(clip.duration)

            # Resize and position the overlay
            overlay_clip = overlay_clip.resize(
                width=clip.w // 2).set_pos(("center", "center"))

            print('Composite the video and overlay')
            # Composite the video and overlay
            composite_clip = CompositeVideoClip([clip, overlay_clip])

            print('Apply video processing effect')
            # Apply video processing
            clip1 = composite_clip.subclip(0, 2).fx(vfx.speedx, 0.5)
            clip2 = composite_clip.subclip(2, 5)
            clip3 = composite_clip.subclip(5, 8).fx(vfx.speedx, 0.5)

            # Concatenate clips
            concate = concatenate_videoclips([clip1, clip2, clip3])

            # Save concatenated clip
            # Use title for file name
            concate_output_path = f"{title}_concate_video.mp4"
            concate.write_videofile(concate_output_path, codec="libx264")

            # Load concatenated clip
            concate_clip = VideoFileClip(concate_output_path)

            # Apply time mirror effect
            reverse_clip = concate_clip.fx(vfx.time_mirror)

            # Concatenate original and reversed clips
            result_clip = concatenate_videoclips([concate_clip, reverse_clip])

            # Generate a random integer based on the current time
            random_integer = int(time.time()) + random.randint(1, 1000)

            # Save final result with a random integer in the filename
            result_clip_output_path = f"{title}_result_{random_integer}.mp4"
            result_clip.write_videofile(
                result_clip_output_path, codec="libx264")

            return jsonify({'message': 'Video processing completed.', 'result_path': result_clip_output_path}), 200
        else:
            return jsonify({'error': 'URL and/or overlay value missing'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
