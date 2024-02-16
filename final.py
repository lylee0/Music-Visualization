import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from pydub import AudioSegment
import moviepy.editor as mp

class Audio():
    def __init__(self, filename = 'Guitar, Loneliness and Blue Planet.wav'):
        self.filename = filename        
        self.sound = AudioSegment.from_file(self.filename)
        self.left = self.sound.split_to_mono()[0]
        self.right = self.sound.split_to_mono()[1]

        self.num_channels = self.sound.channels #==2
        self.frames_per_second = self.sound.frame_rate #==48000
        self.duration = self.sound.duration_seconds #==228.96
        self.size = len(self.sound.get_array_of_samples())

    def addAudio(self):
        add_audio = mp.AudioFileClip(self.filename)
        video1 = mp.VideoFileClip("movie.mp4")
        video1 = video1.subclip(0, 230)
        final = video1.set_audio(add_audio)
        final.write_videofile("final.mp4")

def generateVideo(ani):
    writervideo = FFMpegWriter(fps=50) 
    ani.save('movie.mp4', writer=writervideo)
    plt.close()

def animate(frames):
    '''callback function'''
    slice_left = audio.left.get_sample_slice(frames, frames + window)
    slice_right = audio.right.get_sample_slice(frames, frames + window)

    #plot left channel
    y_left = np.array(slice_left.get_array_of_samples()) / 10000
    if len(y_left)!=0:
        fourier_left = np.abs(np.fft.fft(y_left)) / 60
        left_plot.set_ydata(fourier_left[0:60]) 

    #plot right channel
    y_right = np.array(slice_right.get_array_of_samples()) / 10000
    if len(y_right) != 0:
        fourier_right = np.abs(np.fft.fft(y_right)) / 60
        right_plot.set_ydata(fourier_right[0:60]) 
    return left_plot, right_plot,

if __name__ == "__main__":
    #create audio
    audio = Audio()

    #initilize figure
    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('xkcd:mint green')

    #set axis
    ax = plt.axes(ylim=(0, 10))
    ax.set_axis_off()

    #num_of_frames
    window = int(0.02 * audio.frames_per_second) #960

    #60 points
    left_plot, = ax.plot(np.linspace(0, 10000, 60) , np.zeros(60), 'm*') 

    right_plot, = ax.plot(np.linspace(0, 10000, 60) , np.zeros(60), 'c*')

    ani = FuncAnimation(fig, animate, frames=range(0, audio.size, window), interval=0.01, repeat = False)
    generateVideo(ani)
    audio.addAudio()