# Integration Swiss Meteo Warnings

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Integration to integrate with [swiss_meteo_warnings][swiss_meteo_warnings]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from Swiss Meteo Warnings API.
`switch` | Switch something `True` or `False`.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `swiss_meteo_warnings`.
1. Download _all_ the files from the `custom_components/swiss_meteo_warnings/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Swiss Meteo Warnings"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[swiss_meteo_warnings]: https://github.com/marquisolivier/swiss_meteo_warnings
[commits]: https://github.com/marquisolivier/swiss_meteo_warnings/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/marquisolivier/swiss_meteo_warnings.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/marquisolivier/swiss_meteo_warnings.svg?style=for-the-badge
[releases]: https://github.com/marquisolivier/swiss_meteo_warnings/releases
