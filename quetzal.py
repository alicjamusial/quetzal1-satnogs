import requests
import json


def prepare_file(quetzal_telemetry):
    telemetry_content = ''

    for single in quetzal_telemetry.telemetry:
        telemetry_content += single['frame'][40:]

    telemetry_content_bytearray = bytearray.fromhex(telemetry_content)

    file = open("telemetry.hex", "wb")
    file.write(telemetry_content_bytearray)
    file.close()

    print("\nAll frames count: " + str(len(quetzal_telemetry.telemetry)))


class QuetzalTelemetry:
    def __init__(self, token, start, end):
        self.token = 'Token {}'.format(token)
        self.start = start
        self.end = end

        self.filters = ''

        self.url = "https://db.satnogs.org/api/telemetry/?satellite=99836"

        self.startFrame = "404040404040604040404040406103F0"
        self.lengthFrame = 314

        self.telemetry = []

    def get_and_prepare_telemetry(self):
        self.filters += "&start=" + self.start if self.start else ''
        self.filters += "&end=" + self.end if self.end else ''

        page = 1

        while True:
            url = self.url + "&page=" + str(page) + self.filters
            response = requests.get(url, headers={'Authorization': self.token})

            if response.status_code == 401:
                print("The token is invalid. Try again.")
                exit()

            if response.status_code == 404:
                break

            current_data = json.loads(response.text)
            self.telemetry = self.telemetry + current_data

            page += 1

        self.reverse_telemetry()
        self.filter_telemetry()

    def reverse_telemetry(self):
        self.telemetry = self.telemetry[::-1]

    def filter_telemetry(self):
        self.telemetry = list(
            filter(
                lambda single: single['frame'].startswith(self.startFrame) and len(single['frame']) == self.lengthFrame,
                self.telemetry))
