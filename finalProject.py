from tkinter import *
from tkinter import filedialog, messagebox
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import librosa  
import pygame  
import os

pygame.mixer.init()

INT16_MAX = 32767
NORMALIZATION_FACTOR = 0.95
PLOT_DURATION_SECONDS = 2
MIN_AUDIO_LENGTH_SECONDS = 2
rate = None
data = None
loud_amount = 1.0
pitch_amount = 1.0
amplitude_scale = None
pitch_scale = None
amplitude_value = None
pitch_value = None
next_button = None
fileUpload_window = None

def play_audio(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            return
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
    execute()

def execute():
    global data, rate, loud_amount, pitch_amount
    
    if data is None or rate is None:
        print("Error: No audio data loaded")
        messagebox.showerror("Error", "No audio data loaded")
        return
    
    if len(data) < rate * MIN_AUDIO_LENGTH_SECONDS:
        print(f"Warning: Audio is shorter than {MIN_AUDIO_LENGTH_SECONDS} seconds")
        messagebox.showwarning("Warning", 
                              f"Audio is too short (less than {MIN_AUDIO_LENGTH_SECONDS} seconds). "
                              "Visualization may be incomplete.")
    
    try:
        
        loud = louder(data, loud_amount)
        high = pitch_shift(data, pitch_amount)
        
        
        sf.write('original.wav', (data * INT16_MAX).astype(np.int16), rate)
        sf.write('loud.wav', (loud * INT16_MAX).astype(np.int16), rate)
        sf.write('high_pitch.wav', (high * INT16_MAX).astype(np.int16), rate)
        
        
        plt.figure(figsize=(10, 6))
        
        samples_to_plot = min(rate * PLOT_DURATION_SECONDS, len(data))
        t = np.arange(samples_to_plot) / rate
        
        plt.subplot(3, 1, 1)
        plt.plot(t, data[:samples_to_plot])
        plt.title('Original')
        plt.ylabel('Amplitude')
        
        plt.subplot(3, 1, 2)
        plt.plot(t, loud[:samples_to_plot])
        plt.title('Louder')
        plt.ylabel('Amplitude')
        
        plt.subplot(3, 1, 3)
        plt.plot(t, high[:samples_to_plot])
        plt.title('Higher Pitch')
        plt.ylabel('Amplitude')
        plt.xlabel('Time (seconds)')
        
        plt.tight_layout()
        plt.savefig('plot.png')
        plt.show(block=False)
        
        print("Files saved: original.wav, loud.wav, high_pitch.wav, plot.png")
        print("You can now play the audio files using the playback buttons!")
        
        create_playback_window()
        
    except Exception as e:
        print(f"Error during audio processing: {e}")
        messagebox.showerror("Processing Error", f"An error occurred: {str(e)}")

def create_playback_window():
    global loud_amount, pitch_amount
    
    playback_window = Tk()
    playback_window.geometry("500x200")
    playback_window.title("Audio Playback")
    
    title_label = Label(playback_window, text='Audio Playback Controls', 
                       font=('Arial', 16, 'bold'))
    title_label.pack(pady=20)
    
    button_frame = Frame(playback_window)
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
                      text=f'Amplitude: {loud_amount:.2f} | Pitch: {pitch_amount:.2f}',
                      font=('Arial', 10))
    info_label.pack(pady=10)

def pitch_shift(audio, amount):

    if amount <= 0:
        print("Warning: Invalid pitch amount, using 1.0")
        amount = 1.0
    
    fft = np.fft.fft(audio)
    n = len(fft)
    new = np.zeros(n, dtype=complex)
    
    for i in range(n // 2):
        new_i = int(i * amount)
        if new_i < n // 2:
            new[new_i] += fft[i]
    
    for i in range(n // 2, n):
        original_freq = n - i 
        new_i = n - int(original_freq * amount)
        if new_i >= n // 2 and new_i < n:
            new[new_i] += fft[i]
    
    result = np.fft.ifft(new).real
    
    max_val = np.max(np.abs(result))
    if max_val > 0:
        result = result / max_val * NORMALIZATION_FACTOR
    
    return result

def louder(audio, amount):
    result = audio * amount
    return np.clip(result, -1.0, 1.0)

def submit():
    global loud_amount, pitch_amount
    
    loud_amount = amplitude_scale.get()
    pitch_amount = pitch_scale.get()
    
    amplitude_scale.config(state="disabled")
    pitch_scale.config(state="disabled")
    
    amplitude_value.config(text=f"your amplitude = {loud_amount}")
    pitch_value.config(text=f"your pitch = {pitch_amount}")
    amplitude_value.place(x=250, y=10)
    pitch_value.place(x=250, y=180)
    
def rescale():
    global loud_amount, pitch_amount
    
    loud_amount = 1.0
    pitch_amount = 1.0
    
    amplitude_scale.config(state="normal")
    pitch_scale.config(state="normal")
    amplitude_scale.set(1.0)
    pitch_scale.set(1.0)
    
    amplitude_value.place_forget()
    pitch_value.place_forget()

def next_window():
    global amplitude_scale, pitch_scale, amplitude_value, pitch_value, fileUpload_window
    
    slider_window = Tk()
    slider_window.geometry("700x420")
    
    amplitude = Label(slider_window, text='amplitude:',
                     font=('Arial', 20, 'bold'))
    pitch = Label(slider_window, text='pitch:',
                 font=('Arial', 20, 'bold'))
    amplitude_value = Label(slider_window, text='your amplitude =',
                           font=('Arial', 10))
    pitch_value = Label(slider_window, text='your pitch =',
                       font=('Arial', 10))
    
    amplitude_scale = Scale(slider_window, from_=1, to=2,
                           length=650, orient=HORIZONTAL, 
                           font=('consolas', 20),
                           tickinterval=0.5, resolution=0.01)
    
    pitch_scale = Scale(slider_window, from_=0.5, to=2,
                       length=650, orient=HORIZONTAL, 
                       font=('consolas', 20),
                       tickinterval=0.5, resolution=0.01)
    
    submit_button = Button(slider_window, text='Submit', command=double_func)
    rescale_button = Button(slider_window, text='Rescale', command=rescale)
    
    submit_button.config(font=('Arial', 10, 'bold'),
                        activeforeground='#2b2828',
                        activebackground='grey')
    rescale_button.config(font=('Arial', 10, 'bold'),
                         activeforeground='#2b2828',
                         activebackground='grey')
    
    amplitude.place(x=0, y=0)
    pitch.place(x=0, y=175)
    amplitude_scale.place(x=0, y=45)
    pitch_scale.place(x=0, y=220)
    submit_button.place(x=275, y=375)
    rescale_button.place(x=345, y=375)
    
    fileUpload_window.destroy()

def open_file():
    global rate, data, next_button, fileUpload_window
    
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.wav *.mp3"), 
                  ("WAV files", "*.wav"), 
                  ("MP3 files", "*.mp3")]
    )
    
    if not file_path: 
        return
    
    try:
        print(f"Loading audio file: {file_path}")
        data, rate = librosa.load(file_path, sr=None, mono=True)        
        print("Audio loaded successfully!")
        print(f"Sample rate: {rate}")
        print(f"Data shape: {data.shape}")
        print(f"Duration: {len(data)/rate:.2f} seconds")
        
        duration = f"Duration: {len(data)/rate:.1f} seconds"
        duration_label = Label(fileUpload_window, text=duration,
                              font=('Arial', 10, 'bold'))
        duration_label.place(x=40, y=100)
        
        next_button.config(state="normal")
        
    except Exception as e:
        print(f"Error loading audio file: {e}")
        error_label = Label(fileUpload_window, 
                           text=f"Error: Could not load file",
                           font=('Arial', 10, 'bold'), 
                           fg='red')
        error_label.place(x=40, y=100)
        messagebox.showerror("Load Error", f"Could not load audio file:\n{str(e)}")

def real():
    global next_button, fileUpload_window
    
    fileUpload_window = Tk()
    fileUpload_window.geometry("700x420")
    
    openFile_button = Button(fileUpload_window, text="open", command=open_file)
    next_button = Button(fileUpload_window, text="Next-->", command=next_window)
    label1 = Label(fileUpload_window, text='Choose your file:',
                  font=('Arial', 20, 'bold'))
    
    openFile_button.config(font=('Arial', 12, 'bold'),
                          activeforeground='#2b2828',
                          activebackground='grey')
    next_button.config(font=('Arial', 12, 'bold'),
                      activeforeground='#2b2828',
                      activebackground='grey')
    
    openFile_button.place(x=260, y=12)
    next_button.place(x=310, y=350)
    label1.place(x=10, y=10)
    next_button.config(state="disabled")
    
    main_window.destroy()

def goofy():
    goofy_window = Tk()
    goofy_window.geometry("1000x220")
    
    Label(goofy_window, 
          text='I dont know man remember we are \n "LOST IN SYNC"',
          font=('Arial', 40, 'bold')).pack()
    Label(goofy_window, 
          text='So we cant tell the time',
          font=('Arial', 10, 'bold')).pack()
    
    main_window.destroy()

main_window = Tk() 
main_window.geometry("700x420")

Label(main_window, 
      text='Welcome to Lost in Sync \n program',
      font=('Arial', 40, 'bold')).pack()

button_real = Button(text="Audio Signal Analysis", command=real)
button_goofy = Button(text="what was the time ?!!", command=goofy)

button_real.config(font=('Arial', 30, 'bold'),
                  activeforeground='#2b2828',
                  activebackground='grey',
                  padx=5, pady=10)
button_goofy.config(font=('Arial', 30, 'bold'),
                   activeforeground='#2b2828',
                   activebackground='grey',
                   padx=5, pady=10)

button_real.place(x=120, y=175)
button_goofy.place(x=120, y=300)
  
main_window.mainloop()
