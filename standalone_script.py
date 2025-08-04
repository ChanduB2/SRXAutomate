#!/usr/bin/env python3
"""
Standalone Juniper SRX Configuration Script
Perfect for internship demonstration - works with mock simulation

Usage:
    python standalone_script.py --mock                    # Mock mode (demo)
    python standalone_script.py --host 192.168.1.1       # Real device
"""

import argparse
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def mock_srx_configuration(interface_name='ge-0/0/1', interface_ip='192.168.10.1/24', security_zone='trust'):
    """
    Mock SRX configuration for demonstration purposes
    Simulates all the steps that would happen with a real device
    """
    
    print("=" * 60)
    print("🔥 JUNIPER SRX FIREWALL CONFIGURATION AUTOMATION")
    print("=" * 60)
    print(f"Target Interface: {interface_name}")
    print(f"IP Address: {interface_ip}")
    print(f"Security Zone: {security_zone}")
    print("Mode: MOCK SIMULATION (Safe for Demo)")
    print("=" * 60)
    
    # Configuration steps
    steps = [
        "Connecting to SRX device",
        "Authenticating with device",
        "Creating configuration backup",
        "Loading interface configuration",
        "Configuring IP address",
        "Assigning interface to security zone",
        "Creating security policies for HTTP traffic",
        "Creating security policies for HTTPS traffic",
        "Validating configuration syntax",
        "Committing configuration changes"
    ]
    
    print("\n📋 CONFIGURATION PROCESS:")
    print("-" * 40)
    
    for i, step in enumerate(steps, 1):
        print(f"Step {i:2d}/{len(steps)}: {step}...")
        time.sleep(0.8)  # Realistic timing
        print(f"        ✅ {step} - SUCCESS")
    
    print("\n🎯 APPLIED CONFIGURATION COMMANDS:")
    print("-" * 40)
    
    commands = [
        f"set interfaces {interface_name} unit 0 family inet address {interface_ip}",
        f"set interfaces {interface_name} unit 0 description 'Automated configuration'",
        f"set security zones security-zone {security_zone} interfaces {interface_name}.0",
        "set security policies from-zone trust to-zone untrust policy allow-http match source-address any",
        "set security policies from-zone trust to-zone untrust policy allow-http match destination-address any",
        "set security policies from-zone trust to-zone untrust policy allow-http match application junos-http",
        "set security policies from-zone trust to-zone untrust policy allow-http then permit",
        "set security policies from-zone trust to-zone untrust policy allow-https match source-address any",
        "set security policies from-zone trust to-zone untrust policy allow-https match destination-address any",
        "set security policies from-zone trust to-zone untrust policy allow-https match application junos-https",
        "set security policies from-zone trust to-zone untrust policy allow-https then permit"
    ]
    
    for cmd in commands:
        print(f"  {cmd}")
    
    print("\n" + "=" * 60)
    print("🎉 CONFIGURATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"✅ Interface {interface_name} configured with IP {interface_ip}")
    print(f"✅ Interface assigned to {security_zone} security zone")
    print("✅ Security policies created for HTTP/HTTPS traffic")
    print(f"✅ Configuration committed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 This demonstration shows automated SRX firewall configuration")
    print("   using Python and Junos PyEZ library - perfect for network automation!")
    
    return {
        'success': True,
        'interface': interface_name,
        'ip_address': interface_ip,
        'security_zone': security_zone,
        'commands_applied': len(commands),
        'timestamp': datetime.now().isoformat()
    }

def real_srx_configuration(host, username, password, interface_name, interface_ip, security_zone):
    """
    Real SRX configuration using Junos PyEZ
    """
    try:
        from jnpr.junos import Device
        from jnpr.junos.utils.config import Config
        from jnpr.junos.exception import ConnectError, ConfigLoadError, CommitError
        
        print("=" * 60)
        print("🔥 JUNIPER SRX FIREWALL CONFIGURATION AUTOMATION")
        print("=" * 60)
        print(f"Target Device: {host}")
        print(f"Interface: {interface_name}")
        print(f"IP Address: {interface_ip}")
        print(f"Security Zone: {security_zone}")
        print("Mode: REAL DEVICE")
        print("=" * 60)
        
        # Connect to device
        print(f"\n🔌 Connecting to SRX device at {host}...")
        device = Device(host=host, user=username, password=password, normalize=True)
        device.open()
        device.timeout = 30
        
        # Initialize configuration
        config = Config(device)
        
        print("✅ Connected successfully!")
        print(f"   Device Model: {device.facts.get('model', 'Unknown')}")
        print(f"   JUNOS Version: {device.facts.get('version', 'Unknown')}")
        
        # Generate configuration commands
        commands = [
            f"set interfaces {interface_name} unit 0 family inet address {interface_ip}",
            f"set interfaces {interface_name} unit 0 description 'Automated configuration'",
            f"set security zones security-zone {security_zone} interfaces {interface_name}.0",
            "set security policies from-zone trust to-zone untrust policy allow-http match source-address any",
            "set security policies from-zone trust to-zone untrust policy allow-http match destination-address any",
            "set security policies from-zone trust to-zone untrust policy allow-http match application junos-http",
            "set security policies from-zone trust to-zone untrust policy allow-http then permit",
            "set security policies from-zone trust to-zone untrust policy allow-https match source-address any",
            "set security policies from-zone trust to-zone untrust policy allow-https match destination-address any",
            "set security policies from-zone trust to-zone untrust policy allow-https match application junos-https",
            "set security policies from-zone trust to-zone untrust policy allow-https then permit"
        ]
        
        print("\n📋 Loading configuration...")
        config.load(commands, format='set')
        
        # Show differences
        diff = config.diff()
        if diff:
            print("\n📝 Configuration changes to be applied:")
            print(diff)
        
        # Commit configuration
        print("\n💾 Committing configuration...")
        config.commit(comment=f"Automated SRX configuration - {datetime.now().isoformat()}")
        
        device.close()
        
        print("\n" + "=" * 60)
        print("🎉 REAL DEVICE CONFIGURATION COMPLETED!")
        print("=" * 60)
        
        return {
            'success': True,
            'interface': interface_name,
            'ip_address': interface_ip,
            'security_zone': security_zone,
            'device': host,
            'timestamp': datetime.now().isoformat()
        }
        
    except ImportError:
        print("❌ ERROR: Junos PyEZ library not installed!")
        print("   Install with: pip install junos-eznc")
        return {'success': False, 'error': 'Missing junos-eznc library'}
        
    except ConnectError as e:
        print(f"❌ CONNECTION ERROR: Could not connect to {host}")
        print(f"   Error: {str(e)}")
        print("   Check: IP address, credentials, SSH/NETCONF enabled")
        return {'success': False, 'error': f'Connection failed: {str(e)}'}
        
    except Exception as e:
        print(f"❌ CONFIGURATION ERROR: {str(e)}")
        return {'success': False, 'error': str(e)}

def main():
    parser = argparse.ArgumentParser(
        description='Juniper SRX Firewall Configuration Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python standalone_script.py --mock
  python standalone_script.py --host 192.168.1.1 --user admin --password admin123
  python standalone_script.py --host 10.0.0.1 --interface ge-0/0/2 --ip 10.1.1.1/24
        """
    )
    
    parser.add_argument('--mock', action='store_true', 
                       help='Run in mock mode (simulation for demo)')
    parser.add_argument('--host', help='SRX device IP address')
    parser.add_argument('--user', default='admin', help='Username (default: admin)')
    parser.add_argument('--password', default='admin', help='Password (default: admin)')
    parser.add_argument('--interface', default='ge-0/0/1', 
                       help='Interface name (default: ge-0/0/1)')
    parser.add_argument('--ip', default='192.168.10.1/24', 
                       help='IP address with CIDR (default: 192.168.10.1/24)')
    parser.add_argument('--zone', default='trust', 
                       help='Security zone (default: trust)')
    
    args = parser.parse_args()
    
    if args.mock:
        # Mock mode - perfect for demonstrations
        result = mock_srx_configuration(
            interface_name=args.interface,
            interface_ip=args.ip,
            security_zone=args.zone
        )
    elif args.host:
        # Real device mode
        result = real_srx_configuration(
            host=args.host,
            username=args.user,
            password=args.password,
            interface_name=args.interface,
            interface_ip=args.ip,
            security_zone=args.zone
        )
    else:
        print("❌ ERROR: Must specify either --mock or --host")
        print("Use --help for usage information")
        return
    
    # Summary
    if result['success']:
        print(f"\n🎊 SUCCESS! SRX automation completed in {datetime.now().strftime('%H:%M:%S')}")
    else:
        print(f"\n💥 FAILED! Error: {result.get('error', 'Unknown error')}")

if __name__ == '__main__':
    main()