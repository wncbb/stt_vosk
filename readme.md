# A sst server based on vask-api



## how to run

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
5. make all
6. download model
can find models from [vosk model](https://alphacephei.com/vosk/models)
7. update codes, like change model path and so on
8. try it out
```
#terminal one
python server.py
#terminal two
python client.py --path ./test.mp3
```

Result(use [this model](https://alphacephei.com/vosk/models/vosk-model-small-cn-0.3.zip)):
```
github.com/wncbb/stt_vosk$ python3 client.py --path ./test.mp3 
{
  "error": {
    "msg": "",
    "code": "ERR_SUCCESS"
  },
  "result": {
    "text": "\u6709 \u4e8c \u5e15\u5c14 \u7684 \u8d70\u554a"
  }
}
有 二 帕尔 的 走啊
```

## references
1. [vosk-api github](https://github.com/alphacep/vosk-api)
2. [vosk model](https://alphacephei.com/vosk/models)
3. [kaldi](https://kaldi-asr.org/)
