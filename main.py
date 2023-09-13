from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
import asyncio
import time
import random
from moviepy.editor import *
from fastapi.responses import StreamingResponse

app = FastAPI()


async def generate_progress_updates(total_frames):
    processed_frames = 0
    for frame in range(total_frames):
        # Process your frame here

        processed_frames += 1
        progress = (processed_frames / total_frames) * 100
        yield f"data: {progress:.2f}% processed\n\n"
        # Add a small delay for demonstration purposes
        await asyncio.sleep(0.1)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/progress')
async def progress(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        URL = data.get('URL')
        overlay = data.get('overlay')
        title = data.get('title')

        if URL is not None and overlay is not None and title is not None:
            clip = VideoFileClip(URL)

            # return {"Data": clip}

            total_frames = int(clip.fps * clip.duration)

            # Add your video processing code here
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

            print('Concatenate clips')
            # Concatenate clips
            concate = concatenate_videoclips([clip1, clip2, clip3])

            # Save concatenated clip
            print('Use title for file name')
            # Use title for file name
            concate_output_path = f"{title}_concate_video.mp4"
            concate.write_videofile(concate_output_path, codec="libx264")

            # Load concatenated clip
            print('Load concatenated clip')
            concate_clip = VideoFileClip(concate_output_path)

            # Apply time mirror effect
            print('Apply time mirror effect')
            reverse_clip = concate_clip.fx(vfx.time_mirror)

            # Concatenate original and reversed clips
            print('Concatenate original and reversed clips')
            result_clip = concatenate_videoclips([concate_clip, reverse_clip])

            # Generate a random integer based on the current time
            random_integer = int(time.time()) + random.randint(1, 1000)

            # Save final result with a random integer in the filename
            print('Save final result with a random integer in the filename')
            result_clip_output_path = f"{title}_result_{random_integer}.mp4"
            result_clip.write_videofile(
                result_clip_output_path, codec="libx264")
            # End of video processing code
            print('End of video processing code')
            return {"Success": "true"}
        else:
            raise HTTPException(
                status_code=400, detail='URL, overlay, and/or title value missing')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    from os import getenv

    port = int(getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
