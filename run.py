import sys
from quetzal import QuetzalTelemetry, prepare_file
from zmq_gateway import Uploader

uploader = Uploader('localhost', 7021)

token = None
start = None
end = None

if len(sys.argv) < 2:
    print("No token provided. Type '--help' to get help.")
    exit()

else:
    if sys.argv[1] == '--help':
        print("Usage: python run.py accessToken [startDate] [endDate]")
        print("Date format: %Y-%m-%dT%H:%M:%SZ")
        exit()
    else:
        token = sys.argv[1]

if len(sys.argv) >= 3:
    start = sys.argv[2]

if len(sys.argv) >= 4:
    end = sys.argv[3]


quetzal_telemetry = QuetzalTelemetry(token, start, end)
quetzal_telemetry.get_and_prepare_telemetry()

if True: 
    uploader.upload(quetzal_telemetry.telemetry)
else:
    prepare_file(quetzal_telemetry)