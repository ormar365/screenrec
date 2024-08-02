import pyautogui
import cv2
import pyaudio
import wave
import threading

class ScreenRecorder:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.fps = 12.0
        self.audio_filename = "audio.wav"
        self.video_filename = "screen_recording.avi"

    def record_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(self.audio_filename, 'wb')
        waveFile.setnchannels(2)
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def record_screen(self):
        video = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'XVID'), self.fps, (self.screen_width, self.screen_height))

        while self.recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            video.write(frame)

        video.release()

    def start_recording(self):
        self.recording = True
        audio_thread = threading.Thread(target=self.record_audio)
        screen_thread = threading.Thread(target=self.record_screen)
        audio_thread.start()
        screen_thread.start()

    def stop_recording(self):
        self.recording = False


    def merge_files(self, video_file, audio_file, output_file):
        """
        Merge audio and video files using moviepy.
        
        Args:
        video_file (str): Path to the video file.
        audio_file (str): Path to the audio file.
        output_file (str): Path to the output file.
        """
        try:
            # Load video and audio files
            video = mp.VideoFileClip(video_file)
            audio = mp.AudioFileClip(audio_file)
            
            # Set audio to video
            final_video = video.set_audio(audio)
            
            # Write final video to output file
            final_video.write_videofile(output_file)
            
            # Close files
            video.close()
            audio.close()
            final_video.close()
            
            print(f"Files merged successfully! Output file: {output_file}")
        
        except Exception as e:
            print(f"Error merging files: {e}")