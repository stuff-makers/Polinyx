
# Polinyx

A video-chat application created completely using python.
This is not a normal video-chat application it has been built 
keeping disabled people in mind.
This application has Sign language detection integrated into it.

Currently the application works only on the windows OS with support
from windows 7 onwards

# Run application
1. Clone the project
```
git clone https://github.com/stuff-makers/Polinyx.git
```
2. Install Required Packages
```
pip install -r requirements.txt
```
3. Install pyaudio
```
pip install pyaudio
```
or
```
pipwin install pyaudio
```
4. Build required executables
```
pyinstaller --onefile -w network/video_server.py
pyinstaller --onefile -w network/audio_server.py
```
>You can delete the .spec files and the build folder.

5. Run Polinyx.py
```
python Polinyx.py
```

or 

5. Build Executable
```
pyinstaller -w --collect-all="sklearn" --collect-all="mediapipe" --icon=assets/polinyx.ico Polinyx.py
```
>Copy the UserData, Network, dist and assets folder into the Polinyx folder created in dist. 
>Create a shortcut to the executable or directly run from dist.

