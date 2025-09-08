# HamClock Automations Documentation

This document provides comprehensive information about the automated alert system for the HamClock → Home Assistant bridge.

## Overview

The HamClock automation system provides real-time alerts for significant space weather events, helping amateur radio operators stay informed about propagation conditions and geomagnetic activity.

## Alert Types

### 1. Geomagnetic Storm Alerts

**Trigger:** Kp index ≥ 6
**Purpose:** Alert users to geomagnetic storm conditions that can affect HF propagation

**Configuration:**
```yaml
- alias: "HamClock Alert - High Kp Index"
  trigger:
    - platform: numeric_state
      entity_id: sensor.hamclock_kp_index
      above: 5.9
      for:
        minutes: 5  # Require sustained high values
  action:
    - service: notify.pushover
      data:
        title: "🌩️ HamClock Geomagnetic Storm"
        message: "Kp {{ states('sensor.hamclock_kp_index') }} - Storm conditions!"
        priority: 1
        sound: "spacealarm"
```

**Thresholds:**
- **Minor Storm**: Kp 5-6
- **Moderate Storm**: Kp 7-8
- **Severe Storm**: Kp 9

### 2. Solar Flare Alerts

**Trigger:** X-ray class M or X
**Purpose:** Alert users to significant solar flare activity

**Configuration:**
```yaml
- alias: "HamClock Alert - Major X-ray Flare"
  trigger:
    - platform: state
      entity_id: sensor.hamclock_xray_class
      to: ["M", "X"]
  action:
    - service: notify.pushover
      data:
        title: "☀️ HamClock Solar Flare"
        message: "{{ states('sensor.hamclock_xray_class') }} class flare detected!"
        priority: 1
        sound: "spacealarm"
```

**Classification:**
- **M Class**: Moderate flares (1e-5 to 1e-4 W/m²)
- **X Class**: Major flares (≥ 1e-4 W/m²)

### 3. High Solar Wind Alerts

**Trigger:** Solar wind speed ≥ 600 km/s
**Purpose:** Alert users to high solar wind conditions

**Configuration:**
```yaml
- alias: "HamClock Alert - High Solar Wind"
  trigger:
    - platform: numeric_state
      entity_id: sensor.hamclock_solar_wind_speed
      above: 599
      for:
        minutes: 10  # Require sustained high values
  action:
    - service: notify.pushover
      data:
        title: "💨 HamClock High Solar Wind"
        message: "Solar wind: {{ states('sensor.hamclock_solar_wind_speed') }} km/s"
        priority: 0
        sound: "pushover"
```

### 4. Geomagnetic Coupling Alerts

**Trigger:** Bz GSM ≤ -10 nT
**Purpose:** Alert users to strong geomagnetic coupling conditions

**Configuration:**
```yaml
- alias: "HamClock Alert - Strong South Bz"
  trigger:
    - platform: numeric_state
      entity_id: sensor.hamclock_bz_gsm
      below: -9.9
      for:
        minutes: 5  # Require sustained south values
  action:
    - service: notify.pushover
      data:
        title: "🧲 HamClock Strong Bz South"
        message: "Bz: {{ states('sensor.hamclock_bz_gsm') }} nT - Strong coupling!"
        priority: 1
        sound: "spacealarm"
```

### 5. Propagation Condition Alerts

**Trigger:** SFI < 70 SFU
**Purpose:** Alert users to poor HF propagation conditions

**Configuration:**
```yaml
- alias: "HamClock Alert - Poor Propagation"
  trigger:
    - platform: numeric_state
      entity_id: sensor.hamclock_sfi
      below: 70
      for:
        minutes: 30  # Require sustained poor conditions
  action:
    - service: notify.pushover
      data:
        title: "📻 HamClock Poor Propagation"
        message: "SFI: {{ states('sensor.hamclock_sfi') }} SFU - Poor conditions"
        priority: 0
        sound: "pushover"
```

## Notification Methods

### 1. Pushover Integration

**Setup Requirements:**
- Pushover account and API token
- User/group key configuration
- Sound customization for different alert types

**Configuration:**
```yaml
notify:
  - platform: pushover
    api_key: !secret pushover_api_key
    user_key: !secret pushover_user_key
    name: pushover
```

**Alert Priorities:**
- **Priority 1**: Critical alerts (geomagnetic storms, major flares)
- **Priority 0**: Informational alerts (high solar wind, poor propagation)

### 2. Persistent Notifications

**Purpose:** In-app notifications for Home Assistant users

**Configuration:**
```yaml
- service: notify.persistent_notification
  data:
    title: "🌩️ Geomagnetic Storm Alert"
    message: "Kp index is {{ states('sensor.hamclock_kp_index') }} - Storm conditions!"
    notification_id: "hamclock_kp_storm"
```

### 3. Mobile App Notifications

**Setup:** Configure mobile app notifications through Home Assistant mobile app

**Benefits:**
- Push notifications to mobile devices
- Rich notification content
- Action buttons for quick responses

## Alert Management

### 1. Alert Control

**Enable/Disable Toggle:**
```yaml
input_boolean:
  hamclock_alerts_enabled:
    name: "HamClock Alerts Enabled"
    initial: true
    icon: mdi:bell
```

**Toggle Script:**
```yaml
script:
  hamclock_toggle_alerts:
    alias: "Toggle HamClock Alerts"
    sequence:
      - service: input_boolean.toggle
        entity_id: input_boolean.hamclock_alerts_enabled
```

### 2. Alert Cooldowns

**Implementation:** Use `for:` conditions to prevent alert spam

**Examples:**
- Kp alerts: 5-minute cooldown
- Solar wind alerts: 10-minute cooldown
- Propagation alerts: 30-minute cooldown

### 3. Alert History

**Tracking:** Use notification IDs to prevent duplicate alerts

**Configuration:**
```yaml
notification_id: "hamclock_kp_storm"
```

## Customization Options

### 1. Threshold Adjustment

**Modify Alert Thresholds:**
```yaml
# Change Kp threshold from 6 to 5
above: 4.9  # Instead of 5.9
```

**Add New Thresholds:**
```yaml
# Add warning level for Kp 4-5
- platform: numeric_state
  entity_id: sensor.hamclock_kp_index
  above: 3.9
  below: 5.1
```

### 2. Notification Customization

**Modify Message Content:**
```yaml
message: >
  Custom alert message with {{ states('sensor.hamclock_kp_index') }} Kp
  and {{ states('sensor.hamclock_xray_class') }} flare activity
```

**Change Notification Sounds:**
```yaml
sound: "custom_sound"  # Instead of "spacealarm"
```

### 3. Additional Notification Methods

**Email Notifications:**
```yaml
- service: notify.email
  data:
    title: "HamClock Alert"
    message: "Space weather alert triggered"
```

**SMS Notifications:**
```yaml
- service: notify.sms
  data:
    message: "HamClock alert: {{ states('sensor.hamclock_kp_index') }} Kp"
```

## Testing and Validation

### 1. Manual Testing

**Test Script:**
```yaml
script:
  hamclock_test_alerts:
    alias: "Test HamClock Alerts"
    sequence:
      - service: notify.persistent_notification
        data:
          title: "HamClock Alert Test"
          message: "This is a test of the alert system"
```

### 2. Alert Validation

**Check Points:**
- Verify alert triggers fire correctly
- Confirm notification delivery
- Test alert cooldowns and deduplication
- Validate message content and formatting

### 3. Performance Monitoring

**Metrics to Track:**
- Alert response times
- Notification delivery success rates
- False positive rates
- User engagement with alerts

## Troubleshooting

### Common Issues

1. **Alerts not firing:**
   - Check sensor states and availability
   - Verify automation conditions
   - Test notification services

2. **Duplicate alerts:**
   - Implement proper cooldowns
   - Use notification IDs
   - Check for multiple automation instances

3. **Notification delivery failures:**
   - Verify API keys and credentials
   - Check network connectivity
   - Test notification services independently

### Debugging Steps

1. **Check Home Assistant Logs:**
   ```bash
   tail -f /config/home-assistant.log | grep hamclock
   ```

2. **Test Automation Conditions:**
   - Use Developer Tools to test conditions
   - Verify sensor states and attributes
   - Check automation trigger states

3. **Validate Notification Services:**
   - Test Pushover API connectivity
   - Verify mobile app notifications
   - Check persistent notification display

## Best Practices

### 1. Alert Design
- Use clear, actionable messages
- Include relevant context and data
- Implement appropriate priority levels
- Provide clear alert categorization

### 2. User Experience
- Minimize alert fatigue with smart thresholds
- Provide easy alert management options
- Include helpful context and explanations
- Implement user-friendly alert controls

### 3. Reliability
- Use robust error handling
- Implement proper cooldowns and deduplication
- Monitor alert system performance
- Provide fallback notification methods

## References

- [Home Assistant Automations](https://www.home-assistant.io/docs/automation/)
- [Pushover API Documentation](https://pushover.net/api)
- [Home Assistant Notifications](https://www.home-assistant.io/docs/notifications/)
- [Space Weather Alerts](https://www.swpc.noaa.gov/alerts)
