# Installation Guide

## Quick Start

1. **Add to HACS**:
   - Go to HACS → Frontend → Custom repositories
   - Add repository: `https://github.com/femmeXFMR/home-assistant-HamClock`
   - Set type to **"Template"**
   - Install

2. **Copy Configuration**:
   - Copy `hamclock.yaml` to your `configuration.yaml`
   - Or copy individual package files to your `packages/` directory

3. **Restart Home Assistant**

## Manual Installation

1. **Download Files**:
   - Download all files from `home-assistant/` directory
   - Place in your Home Assistant config directory

2. **Add to configuration.yaml**:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```

3. **Add Dashboards**:
   - Copy dashboard files to your `dashboards/` directory
   - Or add to Lovelace configuration

## Required HACS Integrations

- **ApexCharts Card**: For trend visualizations
- **Mushroom Cards**: For modern card designs
- **Card Mod**: For custom styling

## Data Sources

- **NOAA SWPC**: Space weather data (free, no API key required)
- **Update Interval**: 15 minutes (configurable)
