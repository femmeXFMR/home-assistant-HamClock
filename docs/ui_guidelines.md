# HamClock UI Guidelines

This document provides guidelines for creating and customizing the HamClock Home Assistant dashboard interface.

## Overview

The HamClock bridge provides two main dashboard views:
- **Overview**: Compact view with essential metrics and one chart
- **Details**: Comprehensive view with extended time ranges and detailed data

## Design Principles

### 1. Clarity and Readability
- Use clear, descriptive names for all entities and cards
- Implement consistent color coding across all metrics
- Provide context through units, thresholds, and status indicators

### 2. Mobile Responsiveness
- Design cards to work well on both desktop and mobile devices
- Use responsive grid layouts that adapt to screen size
- Ensure touch targets are appropriately sized

### 3. Visual Hierarchy
- Prioritize the most important metrics in the overview
- Use size, color, and position to guide user attention
- Group related information logically

## Color Coding Standards

### Kp Index (Geomagnetic Activity)
- **Green**: 0-2 (Quiet conditions)
- **Yellow**: 3-4 (Unsettled conditions)
- **Red**: 5-9 (Storm conditions)

### X-ray Class (Solar Flare Activity)
- **Green**: A, B class (Quiet)
- **Yellow**: C class (Minor flares)
- **Orange**: M class (Moderate flares)
- **Red**: X class (Major flares)

### Solar Flux Index (Propagation Conditions)
- **Red**: < 70 SFU (Very poor)
- **Orange**: 70-99 SFU (Poor)
- **Yellow**: 100-149 SFU (Fair)
- **Light Green**: 150-199 SFU (Good)
- **Green**: ≥ 200 SFU (Excellent)

### Solar Wind Speed
- **Green**: < 400 km/s (Low)
- **Yellow**: 400-599 km/s (Moderate)
- **Red**: ≥ 600 km/s (High)

### Bz GSM (Geomagnetic Coupling)
- **Green**: -5 to 5 nT (Neutral)
- **Blue**: ≥ 5 nT (North)
- **Orange**: -10 to -5 nT (Moderate South)
- **Red**: ≤ -10 nT (Strong South)

## Card Types and Usage

### 1. Mushroom Entity Cards
**Use for:** Primary metric display with status indicators

**Configuration:**
```yaml
type: custom:mushroom-entity-card
entity: sensor.hamclock_kp_index
name: "Kp Index"
icon: mdi:magnet
primary_info: state
secondary_info: name
icon_color: |
  [[[
    if (entity.state >= 5) return 'red';
    if (entity.state >= 3) return 'yellow';
    return 'green';
  ]]]
```

### 2. ApexCharts Cards
**Use for:** Historical data visualization and trends

**Configuration:**
```yaml
type: custom:apexcharts-card
graph_span: 48h
update_interval: 5min
series:
  - entity: sensor.hamclock_kp_index
    name: "Kp Index"
    type: line
    stroke_width: 3
    color: "#4488ff"
yaxis:
  - min: 0
    max: 9
    decimals: 1
```

### 3. Entity Cards
**Use for:** Detailed information display and status summaries

**Configuration:**
```yaml
type: entities
title: "Current Status Summary"
entities:
  - entity: sensor.hamclock_kp_status
    name: "Geomagnetic Activity"
  - entity: sensor.hamclock_xray_status
    name: "Solar Flare Activity"
```

### 4. Button Cards
**Use for:** Quick actions and navigation

**Configuration:**
```yaml
type: button
entity: script.hamclock_refresh_all
name: "Refresh Data"
icon: mdi:refresh
tap_action:
  action: call-service
  service: script.hamclock_refresh_all
```

## Layout Guidelines

### Overview Dashboard
- **Header**: Title and refresh button
- **Metrics Grid**: 3-column grid with essential metrics
- **Main Chart**: 48-hour Kp index trend
- **Status Summary**: Current conditions overview
- **Quick Actions**: Navigation and utility buttons

### Details Dashboard
- **Header**: Title and navigation
- **Multi-Chart**: 72-hour overview with multiple metrics
- **Individual Charts**: X-ray flux, SFI, and historical data
- **Detailed Grid**: 2-column grid with comprehensive sensor data
- **Navigation**: Quick access to other views

## Responsive Design

### Grid Layouts
```yaml
type: grid
square: false
columns: 3  # Desktop: 3 columns
# Mobile: automatically reduces to 1-2 columns
```

### Horizontal Stacks
```yaml
type: horizontal-stack
cards:
  - type: button
    entity: script.hamclock_refresh_all
  - type: button
    entity: input_select.hamclock_dashboard_view
```

## Customization Options

### 1. Color Themes
Modify the color coding by updating the `icon_color` templates in Mushroom cards:

```yaml
icon_color: |
  [[[
    if (entity.state >= 5) return 'red';
    if (entity.state >= 3) return 'yellow';
    return 'green';
  ]]]
```

### 2. Chart Customization
Adjust chart appearance through ApexCharts configuration:

```yaml
apex_config:
  chart:
    height: 200
  stroke:
    curve: smooth
  markers:
    size: 4
```

### 3. Layout Modifications
- Change grid columns for different screen sizes
- Adjust card sizes and spacing
- Modify chart time ranges and update intervals

## Accessibility Considerations

### 1. Color Blindness
- Use patterns or icons in addition to colors
- Ensure sufficient contrast ratios
- Provide text alternatives for color-coded information

### 2. Screen Readers
- Use descriptive names and labels
- Provide meaningful entity names
- Include context in card titles and descriptions

### 3. Touch Accessibility
- Ensure buttons and interactive elements are appropriately sized
- Provide clear visual feedback for touch interactions
- Use consistent interaction patterns

## Performance Optimization

### 1. Chart Performance
- Limit chart time ranges to necessary data
- Use appropriate update intervals
- Consider data aggregation for long time ranges

### 2. Card Efficiency
- Minimize the number of cards on each view
- Use efficient templates and conditions
- Avoid unnecessary data processing

### 3. Update Intervals
- Balance real-time updates with performance
- Use appropriate polling intervals for different data types
- Implement smart update strategies

## Troubleshooting UI Issues

### Common Problems
1. **Cards not displaying**: Check entity IDs and card configurations
2. **Colors not updating**: Verify template syntax and entity states
3. **Charts not loading**: Check ApexCharts card configuration and data availability
4. **Mobile layout issues**: Test responsive design and adjust grid columns

### Debugging Steps
1. Check Home Assistant logs for card errors
2. Verify entity states and attributes
3. Test template syntax in Developer Tools
4. Validate card configurations
5. Check for missing custom card dependencies

## Best Practices

### 1. Consistency
- Use consistent naming conventions
- Apply uniform color coding across all metrics
- Maintain consistent layout patterns

### 2. User Experience
- Provide clear navigation between views
- Include helpful context and explanations
- Implement intuitive interaction patterns

### 3. Maintenance
- Document customizations and modifications
- Keep card configurations organized and commented
- Regularly test and validate UI functionality

## References

- [Home Assistant Lovelace UI](https://www.home-assistant.io/lovelace/)
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)
- [ApexCharts Card](https://github.com/RomRider/apexcharts-card)
- [Home Assistant Card Mod](https://github.com/thomasloven/lovelace-card-mod)
