# A sst server base on vask-api



## Before running

1. install python3
2. install ffmpeg
3. use python venv
```
python3 -m venv ./venv
# active virtual environment
source venv/bin/active
```
4. install dependency libraries 
```
# better to upgrade pip first
# otherwise vosk may can not be found 
pip install grpc
pip install grpcio-tools
pip install pydub
pip install vosk
```

## references
1. [vosk-api github](https://github.com/alphacep/vosk-api)
2. [vosk model](https://alphacephei.com/vosk/models)
3. [kaldi](https://kaldi-asr.org/)