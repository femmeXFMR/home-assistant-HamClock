#!/usr/bin/env python3
"""
Simple HamClock Integration Test

This script performs basic validation of the HamClock integration
without requiring external dependencies.
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


def test_endpoint(name, url):
    """Test a single endpoint."""
    print(f"Testing {name} endpoint...")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.status != 200:
                print(f"  ❌ HTTP {response.status}")
                return False
            
            data = json.loads(response.read().decode())
            if not isinstance(data, list) or len(data) == 0:
                print(f"  ❌ Invalid data format")
                return False
            
            latest = data[-1]
            print(f"  ✅ Connected successfully, {len(data)} records")
            print(f"  📊 Latest timestamp: {latest.get('time_tag', 'N/A')}")
            
            # Validate specific fields
            if name == 'kp' and 'kp_index' in latest:
                kp_value = latest['kp_index']
                print(f"  📈 Kp index: {kp_value}")
                if not (0 <= kp_value <= 9):
                    print(f"  ⚠️  Kp value out of expected range")
            
            elif name == 'xray' and 'flux' in latest:
                flux_value = latest['flux']
                print(f"  ☀️  X-ray flux: {flux_value} W/m²")
                if flux_value < 0:
                    print(f"  ⚠️  Negative flux value")
            
            elif name == 'solar_wind' and 'speed' in latest:
                speed_value = latest['speed']
                print(f"  💨 Solar wind: {speed_value} km/s")
                if not (100 <= speed_value <= 1000):
                    print(f"  ⚠️  Speed out of expected range")
            
            elif name == 'bz_gsm' and 'bz_gsm' in latest:
                bz_value = latest['bz_gsm']
                print(f"  🧲 Bz GSM: {bz_value} nT")
                if not (-50 <= bz_value <= 50):
                    print(f"  ⚠️  Bz value out of expected range")
            
            return True
    
    except urllib.error.URLError as e:
        print(f"  ❌ Connection error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False


def test_file_structure():
    """Test that all required files exist."""
    print("Testing file structure...")
    
    required_files = [
        "home-assistant/packages/hamclock_core.yaml",
        "home-assistant/packages/space_weather_kp.yaml",
        "home-assistant/packages/space_weather_xray.yaml",
        "home-assistant/packages/space_weather_sfi.yaml",
        "home-assistant/packages/space_weather_solar_wind.yaml",
        "home-assistant/packages/hamclock_automations.yaml",
        "home-assistant/dashboards/hamclock_overview.yaml",
        "home-assistant/dashboards/hamclock_details.yaml",
        "docs/endpoints.md",
        "docs/ui_guidelines.md",
        "docs/automations.md",
        "README.md"
    ]
    
    success = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - Missing")
            success = False
    
    return success


def main():
    """Main test function."""
    print("HamClock Integration Simple Test")
    print("=" * 40)
    
    # Test endpoints
    endpoints = {
        'kp': 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json',
        'xray': 'https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json',
        'solar_wind': 'https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json',
        'bz_gsm': 'https://services.swpc.noaa.gov/json/ace/mag/ace_mag_1h.json'
    }
    
    endpoint_success = True
    for name, url in endpoints.items():
        if not test_endpoint(name, url):
            endpoint_success = False
        print()
    
    # Test file structure
    file_success = test_file_structure()
    print()
    
    # Summary
    print("=" * 40)
    print("Test Summary:")
    print(f"  Endpoints: {'✅ PASS' if endpoint_success else '❌ FAIL'}")
    print(f"  Files: {'✅ PASS' if file_success else '❌ FAIL'}")
    
    overall_success = endpoint_success and file_success
    print(f"  Overall: {'✅ PASS' if overall_success else '❌ FAIL'}")
    
    if overall_success:
        print("\n🎉 All tests passed! The HamClock integration is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
    
    return 0 if overall_success else 1


if __name__ == '__main__':
    sys.exit(main())
