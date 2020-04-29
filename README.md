## Quetzal-1 & SatNOGS frame downloader

Python3 script to automatically download SatNOGS decoded frames from Quetzal-1 satellite and create `.hex` file that can be uploaded to [Quetzal-1 desktop application](https://github.com/danalvarez/gr-quetzal1).

#### Requirements
- python > 3.5.0
- [access token](https://community.libre.space/t/satnogs-db-telemetry-api-endpoint/5341) for SatNOGS

#### Usage
`python run.py accessToken [startDate] [endDate]`

- *accessToken* - access token to SatNOGS API
- *startDate* - optional, format: `%Y-%m-%dT%H:%M:%SZ`
- *endDate* - optional, format: `%Y-%m-%dT%H:%M:%SZ`