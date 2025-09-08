#!/usr/bin/env python3
"""
HamClock Package Generator

This script generates Home Assistant sensor packages from NOAA space weather endpoints.
It fetches sample data, analyzes schemas, and creates properly configured YAML packages.

Usage:
    python generate_package_from_endpoints.py [options]

Examples:
    # Generate Kp index package
    python generate_package_from_endpoints.py --endpoint kp --output packages/space_weather_kp.yaml
    
    # Generate all packages
    python generate_package_from_endpoints.py --all --output-dir packages/
    
    # Analyze endpoint schema
    python generate_package_from_endpoints.py --analyze --endpoint xray
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class EndpointConfig:
    """Configuration for a NOAA space weather endpoint."""
    
    def __init__(self, name: str, url: str, description: str, 
                 primary_field: str, unit: str, update_freq: str = "1m"):
        self.name = name
        self.url = url
        self.description = description
        self.primary_field = primary_field
        self.unit = unit
        self.update_freq = update_freq


class PackageGenerator:
    """Generates Home Assistant packages from NOAA endpoints."""
    
    def __init__(self):
        self.endpoints = {
            'kp': EndpointConfig(
                name='Kp Index',
                url='https://services.swpc.noaa.gov/json/planetary_k_index_1m.json',
                description='Geomagnetic activity monitoring',
                primary_field='kp_index',
                unit='Kp'
            ),
            'xray': EndpointConfig(
                name='X-ray Flux',
                url='https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json',
                description='Solar flare monitoring',
                primary_field='flux',
                unit='W/m²'
            ),
            'solar_wind': EndpointConfig(
                name='Solar Wind Speed',
                url='https://services.swpc.noaa.gov/json/ace/ace-swepam-1h.json',
                description='Solar wind monitoring',
                primary_field='speed',
                unit='km/s'
            ),
            'bz_gsm': EndpointConfig(
                name='Bz GSM',
                url='https://services.swpc.noaa.gov/json/ace/ace-mag-1h.json',
                description='Geomagnetic coupling monitoring',
                primary_field='bz_gsm',
                unit='nT'
            )
        }
    
    def fetch_endpoint_data(self, endpoint: EndpointConfig) -> Optional[List[Dict]]:
        """Fetch sample data from an endpoint."""
        try:
            with urllib.request.urlopen(endpoint.url) as response:
                data = json.loads(response.read().decode())
                return data if isinstance(data, list) else [data]
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            print(f"Error fetching data from {endpoint.url}: {e}", file=sys.stderr)
            return None
    
    def analyze_schema(self, data: List[Dict], endpoint: EndpointConfig) -> Dict[str, Any]:
        """Analyze the schema of endpoint data."""
        if not data:
            return {}
        
        # Get the most recent entry
        latest = data[-1] if data else {}
        
        schema = {
            'fields': list(latest.keys()),
            'sample_data': latest,
            'data_type': type(latest.get(endpoint.primary_field)).__name__,
            'has_timestamp': 'time_tag' in latest,
            'timestamp_format': 'ISO 8601' if 'time_tag' in latest else None
        }
        
        return schema
    
    def generate_sensor_config(self, endpoint: EndpointConfig, schema: Dict[str, Any]) -> str:
        """Generate REST sensor configuration."""
        sensor_name = f"hamclock_{endpoint.name.lower().replace(' ', '_').replace('-', '_')}"
        
        # Build value template
        if schema.get('has_timestamp'):
            value_template = f"""
        value_template: >
          {{% set last = (value_json | sort(attribute='time_tag') | last) %}}
          {{ (last.{endpoint.primary_field} | float(0) | round(1)) if last else None }}"""
        else:
            value_template = f"""
        value_template: >
          {{ value_json.{endpoint.primary_field} if value_json else None }}"""
        
        # Build attributes
        attributes = ['time_tag'] if schema.get('has_timestamp') else []
        if endpoint.primary_field not in attributes:
            attributes.append(endpoint.primary_field)
        
        config = f"""# HamClock → Home Assistant Bridge
# {endpoint.name} Package
# 
# {endpoint.description}
# Source: {endpoint.url}
# Update frequency: {endpoint.update_freq}

rest:
  - resource: {endpoint.url}
    scan_interval: 900  # 15 minutes - conservative polling
    sensor:
      - name: {sensor_name}
        unique_id: {sensor_name}
{value_template}
        json_attributes_path: "$[-1]"
        json_attributes:
{chr(10).join(f'          - {attr}' for attr in attributes)}
        availability_template: "{{{{ value_json | length > 0 }}}}"
        unit_of_measurement: "{endpoint.unit}"
        device_class: measurement
        state_class: measurement

# Group for organization
group:
  hamclock_{endpoint.name.lower().replace(' ', '_').replace('-', '_')}_group:
    name: "HamClock {endpoint.name}"
    entities:
      - sensor.{sensor_name}
"""
        
        return config
    
    def generate_package(self, endpoint_name: str, output_file: Optional[str] = None) -> bool:
        """Generate a complete package for an endpoint."""
        if endpoint_name not in self.endpoints:
            print(f"Unknown endpoint: {endpoint_name}", file=sys.stderr)
            return False
        
        endpoint = self.endpoints[endpoint_name]
        print(f"Generating package for {endpoint.name}...")
        
        # Fetch sample data
        data = self.fetch_endpoint_data(endpoint)
        if not data:
            print(f"Failed to fetch data from {endpoint.name}", file=sys.stderr)
            return False
        
        # Analyze schema
        schema = self.analyze_schema(data, endpoint)
        print(f"Schema analysis: {len(schema.get('fields', []))} fields found")
        
        # Generate configuration
        config = self.generate_sensor_config(endpoint, schema)
        
        # Write to file
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(config)
            print(f"Package written to {output_path}")
        else:
            print(config)
        
        return True
    
    def generate_all_packages(self, output_dir: str) -> bool:
        """Generate packages for all endpoints."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        success = True
        for endpoint_name in self.endpoints:
            output_file = output_path / f"space_weather_{endpoint_name}.yaml"
            if not self.generate_package(endpoint_name, str(output_file)):
                success = False
        
        return success
    
    def analyze_endpoint(self, endpoint_name: str) -> bool:
        """Analyze and display endpoint schema information."""
        if endpoint_name not in self.endpoints:
            print(f"Unknown endpoint: {endpoint_name}", file=sys.stderr)
            return False
        
        endpoint = self.endpoints[endpoint_name]
        print(f"Analyzing {endpoint.name} endpoint...")
        print(f"URL: {endpoint.url}")
        print(f"Description: {endpoint.description}")
        print(f"Primary field: {endpoint.primary_field}")
        print(f"Unit: {endpoint.unit}")
        print()
        
        # Fetch and analyze data
        data = self.fetch_endpoint_data(endpoint)
        if not data:
            print("Failed to fetch data", file=sys.stderr)
            return False
        
        schema = self.analyze_schema(data, endpoint)
        
        print("Schema Analysis:")
        print(f"  Fields: {', '.join(schema.get('fields', []))}")
        print(f"  Data type: {schema.get('data_type', 'unknown')}")
        print(f"  Has timestamp: {schema.get('has_timestamp', False)}")
        print(f"  Timestamp format: {schema.get('timestamp_format', 'none')}")
        print()
        
        print("Sample Data:")
        sample = schema.get('sample_data', {})
        for key, value in sample.items():
            print(f"  {key}: {value} ({type(value).__name__})")
        
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Home Assistant packages from NOAA space weather endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--endpoint', '-e',
        choices=['kp', 'xray', 'solar_wind', 'bz_gsm'],
        help='Specific endpoint to process'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )
    
    parser.add_argument(
        '--output-dir', '-d',
        help='Output directory for all packages'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Generate packages for all endpoints'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze endpoint schema without generating package'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    generator = PackageGenerator()
    
    # Validate arguments
    if not any([args.endpoint, args.all, args.analyze]):
        parser.error("Must specify --endpoint, --all, or --analyze")
    
    if args.analyze and not args.endpoint:
        parser.error("--analyze requires --endpoint")
    
    if args.all and args.endpoint:
        parser.error("Cannot specify both --all and --endpoint")
    
    # Execute requested action
    success = True
    
    if args.analyze:
        success = generator.analyze_endpoint(args.endpoint)
    elif args.all:
        output_dir = args.output_dir or 'packages'
        success = generator.generate_all_packages(output_dir)
    else:
        success = generator.generate_package(args.endpoint, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
