from tkinter import * 
from tkinter import filedialog
from tkinter import *
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import librosa  
import pygame  

pygame.mixer.init()

BG = "#121212"
CARD = "#1E1E1E"
TXT = "#EAEAEA"

GREEN = "#00E676"
BLUE = "#2979FF"
ORANGE = "#FF9100"
RED = "#FF5252"
CYAN = "#18FFFF"
PURPLE = "#7C4DFF"

def play_audio(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"Playing: {file_path}")
    except Exception as e:
        print(f"Error playing audio: {e}")

def stop_audio():
    pygame.mixer.music.stop()
    print("Playback stopped")

def double_func():
    submit()
    excute()

def excute():
    loud = louder(data, loude_amount)
    high = pitch_shift(data, pitch_amount)
    
    sf.write('original.wav', (data * 32767).astype(np.int16),rate)
    sf.write('loud.wav', (loud * 32767).astype(np.int16),rate)
    sf.write('high_pitch.wav', (high * 32767).astype(np.int16), rate)


    
    plt.figure(figsize=(10, 6))

    t = np.arange(rate*2) / rate

    plt.subplot(3,1,1)
    plt.plot(t, data[:rate*2])
    plt.title('Original')

    plt.subplot(3,1,2)
    plt.plot(t, loud[:rate*2])
    plt.title('Louder')

    plt.subplot(3,1,3)
    plt.plot(t, high[:rate*2])
    plt.title('Higher Pitch')

    plt.tight_layout()
    plt.savefig('plot.png')
    plt.show(block=False)

    print("Files saved: original.wav, loud.wav, high_pitch.wav, plot.png")
    print("You can now play the audio files using the playback buttons!")
    
    create_playback_window()

def create_playback_window():
    playback_window = Tk()
    playback_window.geometry("500x200")
    playback_window.config(bg=BG)
    playback_window.title("Audio Playback")
    
    title_label = Label(playback_window, text='Audio Playback Controls', 
                       font=('Arial', 16, 'bold'),fg=CYAN,bg=BG)
    title_label.pack(pady=20)
    
    button_frame = Frame(playback_window,bg="black")
    button_frame.pack(pady=20)
    
    play_original_btn = Button(button_frame, text='▶ Play Original', 
                               command=lambda: play_audio('original.wav'),
                               font=('Arial', 10, 'bold'), 
                               bg='#4CAF50', fg='white', 
                               padx=10, pady=5)
    play_original_btn.grid(row=0, column=0, padx=5)
    
    play_loud_btn = Button(button_frame, text='▶ Play Louder', 
                          command=lambda: play_audio('loud.wav'),
                          font=('Arial', 10, 'bold'), 
                          bg='#2196F3', fg='white', 
                          padx=10, pady=5)
    play_loud_btn.grid(row=0, column=1, padx=5)
    
    play_pitch_btn = Button(button_frame, text='▶ Play Pitch Shifted', 
                           command=lambda: play_audio('high_pitch.wav'),
                           font=('Arial', 10, 'bold'), 
                           bg='#FF9800', fg='white', 
                           padx=10, pady=5)
    play_pitch_btn.grid(row=0, column=2, padx=5)
    
    stop_btn = Button(button_frame, text='⏹ Stop', 
                     command=stop_audio,
                     font=('Arial', 10, 'bold'), 
                     bg='#f44336', fg='white', 
                     padx=10, pady=5)
    stop_btn.grid(row=1, column=1, padx=5, pady=10)
    
    info_label = Label(playback_window, 
                      text=f'Amplitude: {loude_amount:.2f} | Pitch: {pitch_amount:.2f}',
                      font=('Arial', 10))
    info_label.pack(pady=10)

def pitch_shift(audio, amount):

    
    fft = np.fft.fft(audio)
    n = len(fft)
    new = np.zeros(n, dtype=complex)

    for i in range(n//2):
        new_i = int(i * amount)
        if new_i < n//2:
            new[new_i] += fft[i]  
    
    for i in range(n//2, n):
        original_freq = n - i 
        new_i = n - int(original_freq * amount)
        if new_i >= n//2 and new_i < n:
            new[new_i] += fft[i]  
    
    result = np.fft.ifft(new).real
    
    max_val = np.max(np.abs(result))
    if max_val > 0:
        result = result / max_val * 0.95 
    
    return result


def louder(audio, amount):

    result = audio * amount
    return np.clip(result, -1.0, 1.0) 


def submit():
    global loude_amount
    global pitch_amount
    loude_amount = amplitude_scale.get()
    pitch_amount = pitch_scale.get()
    amplitude_scale.config(state="disabled")
    pitch_scale.config(state="disabled")
    amplitude_value.config(
        text=f"your amplitude = {loude_amount}",
        bg=BG,
        fg="#EAEAEA"
    )
    pitch_value.config(
        text=f"your pitch = {pitch_amount}",
        bg=BG,
        fg="#EAEAEA"
    )
    amplitude_value.place(x=250,y=10)
    pitch_value.place(x=250,y=180)
    
def reScale():
    global loude_amount, pitch_amount
    loude_amount = 1.0
    pitch_amount = 1.0
    amplitude_scale.config(state="normal")
    pitch_scale.config(state="normal")
    amplitude_scale.set(1.0)
    pitch_scale.set(1.0)
    amplitude_value.place_forget()
    pitch_value.place_forget()
    



def next():
    global amplitude_scale, pitch_scale, amplitude_value, pitch_value
    slider_window = Tk()
    slider_window.geometry("700x420")
    slider_window.config(bg=BG)
    amplitude = Label(slider_window,text='amplitude:',
              font=('Arial',20,'bold'),bg=BG, fg=GREEN)
    pitch  = Label(slider_window,text='pitch:',
              font=('Arial',20,'bold'),bg=BG, fg=ORANGE)
    amplitude_value= Label(slider_window,text='your amplitude =',
              font=('Arial',10))
    pitch_value = Label(slider_window,text='your pitch =',
              font=('Arial',10))
    amplitude_scale = Scale(slider_window,from_=1,
              to=2,
              length=650,
              orient=HORIZONTAL, 
              font = ('consolas',20),
              tickinterval=0.5,
              resolution=0.01,
              bg=BG,
              fg=TXT,
              troughcolor=CARD  
              )
    pitch_scale = Scale(slider_window,from_=0.5,
              to=2,
              length=650,
              orient=HORIZONTAL, 
              font = ('consolas',20),
              tickinterval=0.5,
              resolution=0.01,
              bg=BG,
              fg=TXT,
              troughcolor=CARD   
              )
    submit_button = Button(slider_window,text='Submit',command=double_func)
    reScale_button = Button(slider_window,text='Rescale',command=reScale)
    
    submit_button.config(font=('Arial',10,'bold'),
              activeforeground='#2b2828',
              activebackground='grey',
              bg=PURPLE,
              fg='white'
              )
    reScale_button.config(font=('Arial',10,'bold'),
              activeforeground='#2b2828',
              activebackground='grey',
              bg=CYAN,
              fg='black'
              )
    
    amplitude.place(x=0,y=0)
    pitch.place(x=0,y=175)
    amplitude_scale.place(x=0,y=45)
    pitch_scale.place(x=0,y=220)
    submit_button.place(x=275,y=375)
    reScale_button.place(x=345,y=375)
        
    fileUploud_window.destroy()

def openFile():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.wav *.mp3"), ("WAV files", "*.wav"), ("MP3 files", "*.mp3")]
    )
    
    if not file_path: 
        return

    global rate, data

    try:
        print(f"Loading audio file: {file_path}")
        data, rate = librosa.load(file_path, sr=None, mono=True)        
        print("Audio loaded successfully!")
        print("Sample rate:", rate)
        print("Data shape:", data.shape)
        
        Duration = f"Duration: {len(data)/rate:.1f} seconds"
        Duration_lable = Label(fileUploud_window, text=Duration,
                  font=('Arial',10,'bold'),bg=BG,fg="#FFFFFF")
        Duration_lable.place(x=40, y=100)
        next_button.config(state="normal")
        
    except Exception as e:
        print(f"Error loading audio file: {e}")
        error_label = Label(fileUploud_window, text=f"Error: Could not load file",
                  font=('Arial',10,'bold'), fg='red')
        error_label.place(x=40, y=100)


def real():
    global next_button, fileUploud_window
    fileUploud_window = Tk()
    fileUploud_window.geometry("700x420")
    fileUploud_window.config(bg=BG)
    openFile_button = Button(fileUploud_window,text="open",command=openFile)
    next_button = Button(fileUploud_window, text="Next-->",command=next)
    label1 = Label(fileUploud_window,text='Choose your file:',
              font=('Arial',20,'bold'),bg=BG, fg=CYAN)
    openFile_button.config(font=('Arial',12,'bold'),
              activeforeground='#2b2828',
              activebackground='grey',
              bg=GREEN,
              fg='black'
              )
    next_button.config(font=('Arial',12,'bold'),
              activeforeground='#2b2828',
              activebackground='grey',
              bg='BLUE',
              fg='white'
              )
    openFile_button.place(x=260,y=12)
    next_button.place(x=310,y=350)
    label1.place(x=10,y=10)
    next_button.config(state="disabled")
    main_window.destroy()

def goofy():
    goofy_window = Tk()
    goofy_window.geometry("1000x220")
    goofy_window.config(bg=BG)
    goofy1= Label(goofy_window,text='I dont know man remember we are \n "LOST IN SYNC"',
              font=('Arial',40,'bold'),bg=BG, fg=CYAN).pack()
    goofy1= Label(goofy_window,text='So we cant tell the time',
              font=('Arial',10,'bold'),bg=BG, fg='white' ).pack()
    main_window.destroy()



main_window = Tk() 

main_window.geometry("700x420")
main_window.config(bg=BG)

lable3= Label(main_window,text='Welcome to Lost in Sync \n program',
              font=('Arial',40,'bold'),bg=BG, fg=CYAN).pack()


button_real = Button(text="Audio Signal Analysis",bg=PURPLE, fg='white',command=real)
button_gofy = Button(text="what was the time ?!!",bg=PURPLE, fg='white',command=goofy)

button_real.config(font=('Arial',30,'bold'),
              activeforeground='#2b2828',
              activebackground='grey',
              padx=5,
              pady=10
              )
button_gofy.config(font=('Arial',30,'bold'),
              activeforeground='#2b2828',
              activebackground='grey',
              padx=5,
              pady=10
              )

button_real.place(x=120,y=175)
button_gofy.place(x=120,y=300)
  
main_window.mainloop()