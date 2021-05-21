#!/usr/bin/env python3
#
# Copyright 2020 Alpha Cephei Inc
# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""

from concurrent import futures
import os
import sys
import time
import math
import logging
import json
import grpc
from io import BytesIO, StringIO


from pydub import AudioSegment

import stt_service_pb2
import stt_service_pb2_grpc

from vosk import Model, KaldiRecognizer

vosk_interface = os.environ.get('STT_SERVER_IP', '127.0.0.1')
vosk_port = int(os.environ.get('STT_SERVER_PORT', 5001))
vosk_model_path = os.environ.get(
    'STT_MODEL_PATH', 
    './models/vosk-model-small-cn-0.3'
)
vosk_sample_rate = int(os.environ.get('STT_SAMPLE_RATE', 16000))

if len(sys.argv) > 1:
   vosk_model_path = sys.argv[1]

class SttServiceServicer(stt_service_pb2_grpc.SttServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.model = Model(vosk_model_path)

    def get_duration(self, x):
        return x


    def get_response(self, json_resp):
        mid_resp = json.loads(json_resp)
        return stt_service_pb2.RecognizeResponse(
            result=stt_service_pb2.RecognizeResult(text=mid_resp['text']),
            error=stt_service_pb2.Error(msg="", code=stt_service_pb2.ERR_SUCCESS),
        )

    def mp3ToWav(self, mp3_data):
        seg=AudioSegment.from_mp3(BytesIO(mp3_data))
        seg=seg.set_frame_rate(vosk_sample_rate)
        seg=seg.set_channels(1)
        wavIO=BytesIO()
        seg.export(wavIO, format="wav")

        return wavIO.getvalue()

    def Recognize(self, request, context):
        recognizer = KaldiRecognizer(self.model, vosk_sample_rate)

        recognizer.AcceptWaveform(self.mp3ToWav(request.audio_content))
        finalResult = recognizer.FinalResult()
        print(finalResult)
        return self.get_response(finalResult)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor((os.cpu_count() or 1)))
    stt_service_pb2_grpc.add_SttServiceServicer_to_server(
        SttServiceServicer(), server)
    server.add_insecure_port('{}:{}'.format(vosk_interface, vosk_port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

