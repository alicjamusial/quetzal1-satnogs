import argparse
from quetzal import QuetzalTelemetry, prepare_file
from zmq_gateway import Uploader

def main(args):
    quetzal_telemetry = QuetzalTelemetry(args.accessToken, args.startDate, args.endDate)
    quetzal_telemetry.get_and_prepare_telemetry()

    if args.zmq: 
        uploader = Uploader(args.host, args.port)
        uploader.upload(quetzal_telemetry.telemetry)
    else:
        prepare_file(quetzal_telemetry)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('accessToken', help='The Satnogs Access Token')
    parser.add_argument('startDate', nargs="?", help='Start date for observations')
    parser.add_argument('endDate', nargs="?", help='End date for observations')
    parser.add_argument('--host', '-t', help='ZMQ host', default="localhost")
    parser.add_argument('--port', '-p', help='ZMQ port', type=int, default=7021)
    parser.add_argument('--zmq', '-z', help='Use ZMQ endpoint', action='store_true')
    return parser.parse_args()

main(parse_args())
