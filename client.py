

#!/usr/bin/python3

import argparse
import grpc
import json

import stt_service_pb2
import stt_service_pb2_grpc
from google.protobuf.json_format import MessageToJson


CHUNK_SIZE = 8192

def getData(audio_file_name):
    allData=bytes()
    with open(audio_file_name, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        allData=data
        while data != b'':
            data = f.read(CHUNK_SIZE)
            allData=allData+data
    return allData


def run(audio_file_name):
    channel = grpc.insecure_channel('127.0.0.1:5001')
    stub = stt_service_pb2_grpc.SttServiceStub(channel)
    resp=stub.Recognize(stt_service_pb2.RecognizeRequest(audio_content=getData(audio_file_name)))
    print(MessageToJson(resp))
    print(bytes.decode(resp.result.text.encode()))

    

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='audio file path')
    args = parser.parse_args()

    run(args.path)
