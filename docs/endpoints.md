# HamClock Data Endpoints Documentation

This document provides comprehensive information about all data sources used by the HamClock → Home Assistant bridge.

## Overview

The HamClock bridge pulls data from various NOAA (National Oceanic and Atmospheric Administration) services to provide real-time space weather monitoring. All endpoints are publicly accessible and do not require authentication.

## Data Sources

### 1. Planetary K Index (Kp)

**Endpoint:** `https://services.swpc.noaa.gov/json/planetary_k_index_1m.json`

**Purpose:** Geomagnetic activity monitoring

**Update Frequency:** Every 1 minute

**Rate Limit:** No documented limit (conservative 15-minute polling recommended)

**Schema:**
```json
[
  {
    "time_tag": "2024-01-15T12:00:00Z",
    "kp_index": 3.7
  }
]
```

**Fields Used:**
- `time_tag`: ISO 8601 timestamp of measurement
- `kp_index`: Geomagnetic activity index (0-9 scale, unitless)

**Units:** Kp index (unitless, 0-9 scale)

**Classification:**
- 0-2: Quiet
- 3-4: Unsettled  
- 5-6: Minor storm
- 7-8: Moderate storm
- 9: Severe storm

---

### 2. GOES X-ray Flux

**Endpoint:** `https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json`

**Purpose:** Solar flare monitoring

**Update Frequency:** Every 1 minute

**Rate Limit:** No documented limit (conservative 15-minute polling recommended)

**Schema:**
```json
[
  {
    "time_tag": "2024-01-15T12:00:00Z",
    "flux": 1.2e-6
  }
]
```

**Fields Used:**
- `time_tag`: ISO 8601 timestamp of measurement
- `flux`: X-ray flux in W/m²

**Units:** Watts per square meter (W/m²)

**Classification:**
- A class: < 1e-7 W/m²
- B class: 1e-7 to 1e-6 W/m²
- C class: 1e-6 to 1e-5 W/m²
- M class: 1e-5 to 1e-4 W/m²
- X class: ≥ 1e-4 W/m²

---

### 3. Solar Wind Speed (ACE)

**Endpoint:** `https://services.swpc.noaa.gov/json/ace/ace-swepam-1h.json`

**Purpose:** Solar wind monitoring

**Update Frequency:** Every 1 hour

**Rate Limit:** No documented limit (conservative 15-minute polling recommended)

**Schema:**
```json
[
  {
    "time_tag": "2024-01-15T12:00:00Z",
    "speed": 450.2
  }
]
```

**Fields Used:**
- `time_tag`: ISO 8601 timestamp of measurement
- `speed`: Solar wind speed in km/s

**Units:** Kilometers per second (km/s)

**Classification:**
- Low: < 400 km/s
- Moderate: 400-599 km/s
- High: ≥ 600 km/s

---

### 4. Bz GSM (ACE Magnetic Field)

**Endpoint:** `https://services.swpc.noaa.gov/json/ace/ace-mag-1h.json`

**Purpose:** Geomagnetic coupling monitoring

**Update Frequency:** Every 1 hour

**Rate Limit:** No documented limit (conservative 15-minute polling recommended)

**Schema:**
```json
[
  {
    "time_tag": "2024-01-15T12:00:00Z",
    "bz_gsm": -8.5
  }
]
```

**Fields Used:**
- `time_tag`: ISO 8601 timestamp of measurement
- `bz_gsm`: Bz component of magnetic field in GSM coordinates

**Units:** Nanotesla (nT)

**Classification:**
- Strong South: ≤ -10 nT (strong geomagnetic coupling)
- Moderate South: -10 to -5 nT (moderate coupling)
- Neutral: -5 to 5 nT (weak coupling)
- North: ≥ 5 nT (no coupling)

---

## Data Quality and Reliability

### Availability
- All endpoints are maintained by NOAA SWPC (Space Weather Prediction Center)
- Historical uptime is generally >99%
- Data is typically available within 1-5 minutes of measurement

### Data Gaps
- Occasional gaps may occur during satellite maintenance
- Data may be delayed during high solar activity
- Some endpoints may have temporary outages

### Error Handling
- All sensors include `availability_template` guards
- Missing data results in `unavailable` state rather than errors
- Conservative polling intervals minimize impact of temporary outages

## Rate Limiting and Best Practices

### Recommended Polling Intervals
- **Minimum:** 300 seconds (5 minutes)
- **Default:** 900 seconds (15 minutes)
- **Maximum:** 3600 seconds (1 hour)

### Best Practices
1. Use conservative polling intervals to respect NOAA services
2. Implement proper error handling and availability templates
3. Monitor for data quality issues and adjust thresholds as needed
4. Keep historical data for trend analysis and validation

## Alternative Endpoints

### Backup Sources
- **Kp Index:** `https://services.swpc.noaa.gov/json/planetary_k_index_3h.json` (3-hour resolution)
- **X-ray Flux:** `https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json` (3-day history)
- **Solar Wind:** `https://services.swpc.noaa.gov/json/ace/ace-swepam-1d.json` (1-day history)

### Historical Data
- **Kp Index:** `https://services.swpc.noaa.gov/json/planetary_k_index_1m.json` (1-minute resolution)
- **X-ray Flux:** `https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json` (1-day history)
- **Solar Wind:** `https://services.swpc.noaa.gov/json/ace/ace-swepam-1d.json` (1-day history)

## Monitoring and Maintenance

### Health Checks
- Monitor sensor availability and data freshness
- Check for consistent data quality and ranges
- Validate alert thresholds and automation triggers

### Updates and Changes
- NOAA may update endpoint schemas or URLs
- Monitor NOAA SWPC announcements for changes
- Test endpoints regularly to ensure continued functionality

## Troubleshooting

### Common Issues
1. **Sensor shows 'unavailable'**: Check endpoint URL and network connectivity
2. **Data appears stale**: Verify polling intervals and endpoint update frequency
3. **Alerts not firing**: Check automation conditions and sensor states
4. **Inconsistent data**: Validate data ranges and implement additional filtering

### Debugging Steps
1. Check Home Assistant logs for REST sensor errors
2. Verify endpoint URLs are accessible
3. Test data parsing with sample payloads
4. Validate template syntax and logic
5. Check automation conditions and triggers

## References

- [NOAA SWPC Services](https://services.swpc.noaa.gov/)
- [Space Weather Prediction Center](https://www.swpc.noaa.gov/)
- [NOAA ACE Satellite Data](https://www.swpc.noaa.gov/products/ace-real-time-solar-wind)
- [GOES X-ray Data](https://www.swpc.noaa.gov/products/goes-x-ray-flux)
- [Planetary K Index](https://www.swpc.noaa.gov/products/planetary-k-index)
