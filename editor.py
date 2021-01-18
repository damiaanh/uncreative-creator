import ffmpeg
import os
from datetime import date
import random
import shutil

class Editor:

    def __init__(self, path):
        print("Starting editor...")
        self.path = path
        self.editfolder = self.path + "/edited_clips/"
        os.mkdir(self.editfolder)
        self.blurredfolder = self.path + "/blurred_clips/"
        os.mkdir(self.blurredfolder)
        self.addBlurredBackground()
        self.combineSources()
        self.createVideo()

    def combineSources(self):
        for video in os.listdir(self.path+"/blurred_clips/"):
            for audio in os.listdir(self.path+"/audio_only/"):
                try:
                    if str(video) == str(audio):
                        input_video = ffmpeg.input(self.path+"/blurred_clips/"+video)
                        input_audio = ffmpeg.input(self.path+"/audio_only/"+audio)
                        ffmpeg.concat(input_video, input_audio, a=1).output(self.editfolder + str(video)).run()
                except:
                    pass
            if not os.path.isfile(self.path+"/audio_only/"+video):
                shutil.copy2(self.path+"/blurred_clips/"+video, self.editfolder) # copies video to edited folder if it has no sound


    def addBlurredBackground(self):
        # very nice looking blur
        OUTPUT_WIDTH = 1280
        OUTPUT_HEIGHT = 720
        for video in os.listdir(self.path+"/video_only/"):
            try:
                input_video = ffmpeg.input(self.path+"/video_only/"+video)
                probe = ffmpeg.probe(self.path+"/video_only/"+video)
                video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
                input_width = int(video_stream["width"])
                input_height = int(video_stream["height"])
                nw = OUTPUT_HEIGHT*input_width/input_height
                (
                    ffmpeg
                    .overlay(
                        input_video.filter("scale", OUTPUT_WIDTH, -2).crop(0,(OUTPUT_WIDTH*OUTPUT_HEIGHT/nw-OUTPUT_HEIGHT)/2,OUTPUT_WIDTH, OUTPUT_HEIGHT).filter("gblur", sigma=40),
                        input_video.filter("scale", -2, OUTPUT_HEIGHT),
                        x=(OUTPUT_WIDTH-nw)/2
                    )
                    .output(self.blurredfolder + video)
                    .run()
                )
            except:
                pass

    def createVideo(self):
        videos = []
        for video in os.listdir(self.path+"/edited_clips/"):
            videos.append(ffmpeg.input(self.path+"/edited_clips/"+video))
        random.shuffle(videos)
        ffmpeg.concat(*videos, unsafe=True).output(self.path + "/edited.mp4").run()

