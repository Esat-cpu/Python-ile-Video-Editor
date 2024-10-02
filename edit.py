from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, vfx, afx
from os.path import exists

clip = ""

class Edit:
    def sesekleme(self, videoadi, sesadi, f1, f2):
        global clip
        if not clip:
            if not exists(videoadi) or not exists(sesadi): raise NameError
            clip = VideoFileClip(videoadi)
        audio = AudioFileClip(sesadi)

        if f1: audio = audio.fx(afx.fadein, 1)
        if f2: audio = audio.fx(afx.fadeout, 1)

        clip.audio = CompositeAudioClip([audio])

    
    def birlestir(self, video1adi, video2adi, f1, f2):
        global clip
        if not clip:
            if not exists(video1adi) or not exists(video2adi): raise NameError
            klip1 = VideoFileClip(video1adi)
        else: klip1 = clip
        klip2 = VideoFileClip(video2adi)

        if f1: klip1 = klip1.fx(vfx.fadeout, 1)
        if f2: klip2 = klip2.fx(vfx.fadein, 1)
        clip = concatenate_videoclips([klip1, klip2])


    def kirp(self, videoadi: str, zaman1, zaman2):
        global clip
        if not clip:
            if not exists(videoadi): raise NameError
            if videoadi.endswith(".mp4"):
                clip = VideoFileClip(videoadi)
            elif videoadi.endswith(".mp3"):
                clip = AudioFileClip(videoadi)
        clip = clip.subclip(zaman1, zaman2)

    def yazdir(self, isim=""):
        klip = clip
        self.clip0()
        ad = isim + ".mp4"
        if isim.endswith(".mp3"): ad = isim
        if not isim:
            sayac = ""
            while exists(f"Video{sayac}.mp4"):
                if not sayac: sayac = 1
                sayac += 1
            ad = f"Video{sayac}.mp4"
        try: klip.write_videofile(ad)
        except:
            try: klip.write_audiofile(ad)
            except: klip.write_audiofile(ad[:-4] + ".mp3")

    def clip0(self):
        global clip
        clip = ""
    def clipsorgu(self):
        if clip: return True
        else: return False
