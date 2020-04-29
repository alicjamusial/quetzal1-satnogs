from typing import List

import zmq


class Uploader:
    def __init__(self, host : str,  port: int):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.address = f'tcp://{host}:' + str(port)
        self.socket.connect(self.address)

    def upload(self, frames: List[bytes]):
        for frame in frames:
            frame_data = bytes.fromhex(frame['frame'])
            payload = frame_data[16:]
            self.socket.send(payload)
