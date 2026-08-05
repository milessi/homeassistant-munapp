# MunApp School Transport

A Home Assistant integration for the Finnish **MunApp** school transport service.

Monitor your children's school transport schedules, manage transport cancellations, and view upcoming transports directly in Home Assistant.

## Features

- 🚌 View today's and tomorrow's school transports
- 📅 Calendar integration with weekly transport schedule
- 🔄 Cancel and restore transports directly from Home Assistant
- 🔔 View MunApp notifications
- 👨‍👩‍👧‍👦 Supports multiple children
- ⚙️ Config Flow setup
- 📦 HACS compatible
- 🇫🇮 Designed for Finnish MunApp users

## Entities

The integration creates:

- Sensors
  - Child information
  - Next transport details
- Binary sensors
  - Transport available today
- Switches
  - Today Morning Transport
  - Today Afternoon Transport
  - Tomorrow Morning Transport
  - Tomorrow Afternoon Transport
- Buttons
  - Manual refresh
- Calendar
  - Weekly school transport schedule

## Calendar

The integration creates one calendar per child.

Calendar events include:

- 🚌 x Kid → School
- 🚌 x Kid → Home

Each event contains additional information:

- Route
- Vehicle
- School
- Pickup / destination address

## Installation

### HACS

1. Open **HACS**.
2. Add this repository as a **Custom Repository**.
3. Category: **Integration**.
4. Install **MunApp School Transport**.
5. Restart Home Assistant.
6. Add the integration from **Settings → Devices & Services**.

## Requirements

- Home Assistant
- Active MunApp account
- Internet connection

## Screenshots

*(Screenshots coming soon.)*

## Development

```bash
git clone git@github.com:milessi/ha-munapp-school-transport.git
```
Will add future features as they appear


## License

MIT License
