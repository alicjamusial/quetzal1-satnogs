import argparse
import logging
import time
import colorlog

import zmq

def _setup_log(silent):
    root_logger = logging.getLogger()

    handler = colorlog.StreamHandler()

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)-15s %(levelname)s: [%(name)s] %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    if silent:
        root_logger.setLevel(logging.INFO)
    else:
        root_logger.setLevel(logging.DEBUG)


def main(args):
    _setup_log(args.silent)
    log = logging.getLogger()

    context = zmq.Context()
    socket_upload = context.socket(zmq.PUB)
    address_upload = f'tcp://{args.host}:{args.port_upload}' 
    socket_upload.bind(address_upload)

    socket_listener = context.socket(zmq.SUB)
    address_listener = f'tcp://{args.host}:{args.port_listener}'  
    socket_listener.bind(address_listener) 
    socket_listener.setsockopt(zmq.RCVTIMEO, 1000)
    socket_listener.setsockopt(zmq.SUBSCRIBE, b"")


    log.info("Listening.")

    time.sleep(0.5)

    while True:							
        try:
            data = socket_listener.recv()
            log.debug("Received packet, length %d", len(data))
            socket_upload.send(data)
        except zmq.Again:
            continue													
        except KeyboardInterrupt:
            break
            
    socket_listener.close()
    socket_upload.close()
    log.info("Disconnected.")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-t', help='Host', default='*')
    parser.add_argument('--port_upload', '-u', help='Upload port', type=int, default=7020)
    parser.add_argument('--port_listener', '-l', help='Listener port', type=int, default=7021)
    parser.add_argument('--silent', '-s', help='Silent logging', action='store_true')
    return parser.parse_args()

main(parse_args())
