# HamClock → Home Assistant Bridge

A comprehensive Home Assistant integration that replicates HamClock's space weather monitoring capabilities as native sensors, modern dashboards, and automated alerts.

> **Inspired by [HamClock](https://github.com/softerhardware/HamClock)** by Robert L. Read - A beautiful space weather kiosk for amateur radio operators. This integration brings HamClock's functionality to Home Assistant with modern dashboards and automation capabilities.

## 🌟 Features

- **Real-time Space Weather Monitoring**: Kp index, X-ray flux, solar flux index, and solar wind data
- **Modern Lovelace Dashboards**: ApexCharts visualizations and Mushroom card interfaces
- **Automated Alerts**: Pushover notifications for geomagnetic storms, solar flares, and propagation changes
- **Comprehensive Documentation**: Detailed setup guides, API documentation, and troubleshooting
- **Modular Architecture**: Organized packages for easy customization and maintenance

## 📊 Monitored Metrics

### Geomagnetic Activity
- **Kp Index**: 0-9 scale geomagnetic activity (NOAA planetary K index)
- **Bz GSM**: Geomagnetic coupling component (ACE satellite data)

### Solar Activity
- **X-ray Flux**: Solar flare monitoring (GOES satellite data)
- **X-ray Class**: A, B, C, M, X flare classification
- **Solar Flux Index**: HF propagation conditions (SFI)

### Solar Wind
- **Wind Speed**: Solar wind velocity (ACE satellite data)
- **Activity Status**: Low, moderate, high classification

## 🚀 Quick Start

### 1. Installation

1. Copy the `home-assistant/` directory contents to your Home Assistant configuration
2. Ensure you have the required custom cards installed:
   - [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)
   - [ApexCharts Card](https://github.com/RomRider/apexcharts-card)
   - [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### 2. Configuration

Add the core package to your `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages

# Include HamClock packages
packages:
  hamclock_core: !include packages/hamclock_core.yaml
```

### 3. Dashboard Setup

1. Go to **Configuration** → **Dashboards**
2. Click **+ ADD DASHBOARD** → **Import**
3. Import the dashboard files from `dashboards/` directory

### 4. Alert Configuration (Optional)

For Pushover notifications, add to your `secrets.yaml`:

```yaml
pushover_api_key: "your_api_key_here"
pushover_user_key: "your_user_key_here"
```

## 📁 Project Structure

```
home-assistant/
├── packages/
│   ├── hamclock_core.yaml           # Main package with all sensors
│   ├── space_weather_kp.yaml        # Kp index and geomagnetic data
│   ├── space_weather_xray.yaml      # X-ray flux and flare classification
│   ├── space_weather_sfi.yaml       # Solar flux index
│   ├── space_weather_solar_wind.yaml # Solar wind and Bz GSM data
│   └── hamclock_automations.yaml    # Automated alerts and notifications
├── dashboards/
│   ├── hamclock_overview.yaml       # Compact overview dashboard
│   └── hamclock_details.yaml        # Detailed analysis dashboard
└── docs/
    ├── endpoints.md                 # Data source documentation
    ├── ui_guidelines.md             # Dashboard customization guide
    └── automations.md               # Alert system documentation
```

## 🎨 Dashboard Views

### Overview Dashboard
- **Essential Metrics**: Kp, X-ray class, SFI, solar wind in a compact grid
- **48-Hour Kp Chart**: ApexCharts visualization with trend analysis
- **Status Summary**: Current conditions overview
- **Quick Actions**: Refresh data and navigation controls

### Details Dashboard
- **Multi-Metric Chart**: 72-hour overview with multiple space weather indicators
- **Individual Charts**: X-ray flux, SFI, and historical data analysis
- **Comprehensive Data**: Detailed sensor information and attributes
- **Extended Time Ranges**: 7-day and 30-day historical analysis

## 🔔 Alert System

### Automated Notifications
- **Geomagnetic Storms**: Kp ≥ 6 with 5-minute cooldown
- **Solar Flares**: M/X class flares with immediate notification
- **High Solar Wind**: Speed ≥ 600 km/s with 10-minute cooldown
- **Poor Propagation**: SFI < 70 with 30-minute cooldown
- **Daily Summary**: 8 AM UTC space weather overview

### Notification Methods
- **Pushover**: High-priority alerts with custom sounds
- **Persistent Notifications**: In-app Home Assistant notifications
- **Mobile App**: Push notifications to mobile devices

## 🛠️ Customization

### Threshold Adjustment
Modify alert thresholds in `packages/hamclock_automations.yaml`:

```yaml
# Change Kp storm threshold from 6 to 5
above: 4.9  # Instead of 5.9
```

### Color Coding
Customize UI colors in dashboard files:

```yaml
icon_color: |
  [[[
    if (entity.state >= 5) return 'red';
    if (entity.state >= 3) return 'yellow';
    return 'green';
  ]]]
```

### Chart Customization
Adjust ApexCharts configuration:

```yaml
apex_config:
  chart:
    height: 200
  stroke:
    curve: smooth
  markers:
    size: 4
```

## 📚 Documentation

- **[Endpoints Documentation](docs/endpoints.md)**: Complete API reference and data source information
- **[UI Guidelines](docs/ui_guidelines.md)**: Dashboard customization and design principles
- **[Automations Guide](docs/automations.md)**: Alert system configuration and troubleshooting

## 🔧 Troubleshooting

### Common Issues

1. **Sensors showing 'unavailable'**:
   - Check network connectivity
   - Verify NOAA endpoint accessibility
   - Review Home Assistant logs

2. **Charts not loading**:
   - Ensure ApexCharts card is installed
   - Check sensor data availability
   - Verify chart configuration

3. **Alerts not firing**:
   - Check automation conditions
   - Verify notification service configuration
   - Test alert triggers manually

### Debugging Steps

1. **Check Logs**:
   ```bash
   tail -f /config/home-assistant.log | grep hamclock
   ```

2. **Test Sensors**:
   - Go to **Developer Tools** → **States**
   - Search for `hamclock_` entities
   - Verify sensor states and attributes

3. **Validate Automations**:
   - Go to **Configuration** → **Automations**
   - Check automation states and triggers
   - Test automation conditions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines

- Follow the established naming conventions
- Include comprehensive documentation
- Test all changes with real data
- Maintain backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HamClock**: Original space weather monitoring application
- **NOAA SWPC**: Space weather data and services
- **Home Assistant Community**: Custom cards and integrations
- **Amateur Radio Community**: Feedback and testing

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions for help and ideas
- **Documentation**: Check the comprehensive docs for detailed information

## 🔗 Related Projects

- [HamClock](http://www.clearskyinstitute.com/ham/HamClock) - Original application
- [NOAA SWPC](https://www.swpc.noaa.gov/) - Space weather data source
- [Home Assistant](https://www.home-assistant.io/) - Home automation platform

---

**Note**: This integration is not affiliated with or endorsed by the original HamClock project. It is an independent Home Assistant implementation inspired by HamClock's space weather monitoring capabilities.
