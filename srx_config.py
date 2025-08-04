#!/usr/bin/env python3
"""
Juniper SRX Configuration Module using Junos PyEZ
This module provides functionality to configure Juniper SRX firewalls
"""

import logging
from datetime import datetime
import xml.etree.ElementTree as ET

try:
    from jnpr.junos import Device
    from jnpr.junos.utils.config import Config
    from jnpr.junos.exception import ConnectError, ConfigLoadError, CommitError
    JUNOS_PYEZ_AVAILABLE = True
except ImportError:
    JUNOS_PYEZ_AVAILABLE = False
    logging.warning("Junos PyEZ not available. Mock mode will be used.")

logger = logging.getLogger(__name__)

class SRXConfigurator:
    """Main class for SRX firewall configuration automation"""
    
    def __init__(self, host, user, password, port=22, timeout=30):
        """
        Initialize SRX configurator
        
        Args:
            host (str): SRX device IP address
            user (str): Username for authentication
            password (str): Password for authentication
            port (int): SSH port (default: 22)
            timeout (int): Connection timeout in seconds
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.timeout = timeout
        self.device = None
        self.config = None
        
        if not JUNOS_PYEZ_AVAILABLE:
            raise ImportError("Junos PyEZ library is not available. Please install junos-eznc.")
    
    def connect(self):
        """Establish connection to SRX device"""
        try:
            logger.info(f"Connecting to SRX device at {self.host}")
            
            self.device = Device(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                normalize=True,
                gather_facts=True
            )
            
            self.device.open()
            self.device.timeout = self.timeout
            
            # Initialize configuration utility
            self.config = Config(self.device)
            
            logger.info(f"Successfully connected to {self.host}")
            return True
            
        except ConnectError as e:
            logger.error(f"Failed to connect to {self.host}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected connection error: {str(e)}")
            raise
    
    def disconnect(self):
        """Close connection to SRX device"""
        if self.device:
            try:
                self.device.close()
                logger.info(f"Disconnected from {self.host}")
            except Exception as e:
                logger.warning(f"Error during disconnect: {str(e)}")
    
    def get_device_info(self):
        """Get basic device information"""
        if not self.device:
            self.connect()
        
        try:
            facts = self.device.facts
            return {
                'hostname': facts.get('hostname', 'unknown'),
                'model': facts.get('model', 'unknown'),
                'version': facts.get('version', 'unknown'),
                'serial': facts.get('serialnumber', 'unknown'),
                'uptime': str(facts.get('RE0', {}).get('up_time', 'unknown'))
            }
        except Exception as e:
            logger.error(f"Failed to get device info: {str(e)}")
            raise
    
    def backup_configuration(self):
        """Create a backup of current configuration"""
        if not self.device:
            self.connect()
        
        try:
            logger.info("Creating configuration backup")
            
            # Get current configuration
            config_xml = self.device.rpc.get_config(format='xml')
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'device_ip': self.host,
                'configuration': ET.tostring(config_xml, encoding='unicode')
            }
            
            logger.info("Configuration backup created successfully")
            return backup_data
            
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            raise
    
    def configure_interface_and_policy(self, interface_name='ge-0/0/1', 
                                     interface_ip='192.168.10.1/24', 
                                     security_zone='trust'):
        """
        Configure interface with IP address, assign to security zone,
        and create security policy for HTTP traffic
        
        Args:
            interface_name (str): Interface to configure (default: ge-0/0/1)
            interface_ip (str): IP address with CIDR (default: 192.168.10.1/24)
            security_zone (str): Security zone assignment (default: trust)
        
        Returns:
            dict: Configuration result with success status and details
        """
        
        if not self.device:
            self.connect()
        
        try:
            logger.info(f"Starting configuration for interface {interface_name}")
            
            # Create configuration commands
            config_commands = self._generate_config_commands(
                interface_name, interface_ip, security_zone
            )
            
            # Load configuration
            logger.info("Loading configuration...")
            self.config.load(config_commands, format='set')
            
            # Show configuration differences
            diff = self.config.diff()
            if diff:
                logger.info(f"Configuration changes:\n{diff}")
            else:
                logger.info("No configuration changes detected")
            
            # Commit configuration
            logger.info("Committing configuration...")
            self.config.commit(comment=f"SRX automation - {datetime.now().isoformat()}")
            
            result = {
                'success': True,
                'message': 'Configuration applied successfully',
                'details': {
                    'interface': interface_name,
                    'ip_address': interface_ip,
                    'security_zone': security_zone,
                    'changes': diff,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            logger.info("Configuration completed successfully")
            return result
            
        except ConfigLoadError as e:
            logger.error(f"Configuration load error: {str(e)}")
            return {
                'success': False,
                'message': f'Configuration load failed: {str(e)}',
                'details': {}
            }
        except CommitError as e:
            logger.error(f"Configuration commit error: {str(e)}")
            return {
                'success': False,
                'message': f'Configuration commit failed: {str(e)}',
                'details': {}
            }
        except Exception as e:
            logger.error(f"Unexpected configuration error: {str(e)}")
            return {
                'success': False,
                'message': f'Configuration failed: {str(e)}',
                'details': {}
            }
    
    def _generate_config_commands(self, interface_name, interface_ip, security_zone):
        """
        Generate Junos set commands for interface and security configuration
        
        Args:
            interface_name (str): Interface name
            interface_ip (str): IP address with CIDR
            security_zone (str): Security zone name
        
        Returns:
            list: List of Junos set commands
        """
        
        commands = [
            # Interface configuration
            f"set interfaces {interface_name} unit 0 family inet address {interface_ip}",
            f"set interfaces {interface_name} unit 0 description 'Automated configuration'",
            
            # Security zone configuration
            f"set security zones security-zone {security_zone} interfaces {interface_name}.0",
            
            # Security policy for HTTP traffic from trust to untrust
            "set security policies from-zone trust to-zone untrust policy allow-http match source-address any",
            "set security policies from-zone trust to-zone untrust policy allow-http match destination-address any",
            "set security policies from-zone trust to-zone untrust policy allow-http match application junos-http",
            "set security policies from-zone trust to-zone untrust policy allow-http then permit",
            
            # Security policy for HTTPS traffic from trust to untrust
            "set security policies from-zone trust to-zone untrust policy allow-https match source-address any",
            "set security policies from-zone trust to-zone untrust policy allow-https match destination-address any",
            "set security policies from-zone trust to-zone untrust policy allow-https match application junos-https",
            "set security policies from-zone trust to-zone untrust policy allow-https then permit",
            
            # Basic security zones if they don't exist
            "set security zones security-zone trust host-inbound-traffic system-services ssh",
            "set security zones security-zone trust host-inbound-traffic system-services ping",
            "set security zones security-zone untrust screen untrust-screen",
        ]
        
        logger.info(f"Generated {len(commands)} configuration commands")
        return commands
    
    def validate_configuration(self):
        """Validate current configuration"""
        if not self.device:
            self.connect()
        
        try:
            # Check configuration syntax
            self.config.commit_check()
            logger.info("Configuration validation successful")
            return True
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return False
    
    def rollback_configuration(self, rollback_id=1):
        """Rollback to previous configuration"""
        if not self.device:
            self.connect()
        
        try:
            logger.info(f"Rolling back configuration (rollback {rollback_id})")
            self.config.rollback(rollback_id)
            self.config.commit(comment=f"Rollback {rollback_id} - {datetime.now().isoformat()}")
            
            logger.info("Configuration rollback completed")
            return {
                'success': True,
                'message': f'Rolled back to previous configuration ({rollback_id})',
                'details': {'rollback_id': rollback_id}
            }
            
        except Exception as e:
            logger.error(f"Rollback failed: {str(e)}")
            return {
                'success': False,
                'message': f'Rollback failed: {str(e)}',
                'details': {}
            }
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

# Standalone script functionality
def main():
    """Main function for standalone script execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Juniper SRX Configuration Automation')
    parser.add_argument('--host', required=True, help='SRX device IP address')
    parser.add_argument('--user', default='admin', help='Username')
    parser.add_argument('--password', default='admin', help='Password')
    parser.add_argument('--interface', default='ge-0/0/1', help='Interface name')
    parser.add_argument('--ip', default='192.168.10.1/24', help='IP address with CIDR')
    parser.add_argument('--zone', default='trust', help='Security zone')
    parser.add_argument('--backup', action='store_true', help='Create backup before configuration')
    
    args = parser.parse_args()
    
    try:
        with SRXConfigurator(args.host, args.user, args.password) as configurator:
            # Create backup if requested
            if args.backup:
                backup = configurator.backup_configuration()
                print(f"Backup created: {backup['timestamp']}")
            
            # Apply configuration
            result = configurator.configure_interface_and_policy(
                interface_name=args.interface,
                interface_ip=args.ip,
                security_zone=args.zone
            )
            
            if result['success']:
                print("Configuration applied successfully!")
                print(f"Interface: {args.interface}")
                print(f"IP Address: {args.ip}")
                print(f"Security Zone: {args.zone}")
            else:
                print(f"Configuration failed: {result['message']}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
