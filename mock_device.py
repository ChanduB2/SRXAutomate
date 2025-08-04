#!/usr/bin/env python3
"""
Mock SRX Device Simulator
This module provides mock simulation capabilities for testing
SRX configuration without actual hardware
"""

import logging
import time
from datetime import datetime
import random
import json

logger = logging.getLogger(__name__)

class MockSRXDevice:
    """Mock SRX device for simulation and testing"""
    
    def __init__(self):
        """Initialize mock SRX device with default state"""
        self.hostname = "vSRX-Mock"
        self.model = "vSRX"
        self.version = "20.4R3.8"
        self.serial = "VM123456789"
        self.uptime = "45 days, 12:34:56"
        
        # Mock device state
        self.interfaces = {
            'ge-0/0/0': {
                'status': 'up',
                'ip': '10.0.0.1/24',
                'zone': 'untrust',
                'description': 'WAN Interface'
            },
            'ge-0/0/1': {
                'status': 'down',
                'ip': 'unassigned',
                'zone': None,
                'description': 'LAN Interface'
            }
        }
        
        self.security_zones = {
            'trust': {
                'interfaces': [],
                'policies': []
            },
            'untrust': {
                'interfaces': ['ge-0/0/0.0'],
                'policies': []
            }
        }
        
        self.security_policies = []
        
        # Configuration history
        self.config_history = []
        
        logger.info("Mock SRX device initialized")
    
    def get_device_info(self):
        """Return mock device information"""
        return {
            'hostname': self.hostname,
            'model': self.model,
            'version': self.version,
            'serial': self.serial,
            'uptime': self.uptime,
            'mock_mode': True
        }
    
    def simulate_connection(self, delay=2):
        """Simulate connection establishment with realistic delay"""
        logger.info("Simulating connection to mock SRX device...")
        
        # Simulate connection time
        time.sleep(delay)
        
        # Simulate occasional connection failures (5% chance)
        if random.random() < 0.05:
            raise ConnectionError("Mock connection failed (simulated network issue)")
        
        logger.info("Mock connection established successfully")
        return True
    
    def simulate_configuration(self, interface_name='ge-0/0/1', 
                             interface_ip='192.168.10.1/24', 
                             security_zone='trust'):
        """
        Simulate SRX configuration process
        
        Args:
            interface_name (str): Interface to configure
            interface_ip (str): IP address with CIDR
            security_zone (str): Security zone assignment
        
        Returns:
            dict: Configuration result
        """
        
        try:
            logger.info(f"Starting mock configuration for interface {interface_name}")
            
            # Simulate connection
            self.simulate_connection(delay=1)
            
            # Simulate configuration steps
            config_steps = [
                "Backing up current configuration",
                "Loading interface configuration",
                "Configuring IP address",
                "Assigning to security zone",
                "Creating security policies",
                "Validating configuration",
                "Committing changes"
            ]
            
            completed_steps = []
            
            for i, step in enumerate(config_steps, 1):
                logger.info(f"Step {i}/{len(config_steps)}: {step}")
                
                # Simulate processing time
                time.sleep(0.5)
                
                # Simulate occasional step failures (2% chance per step)
                if random.random() < 0.02:
                    error_msg = f"Mock error during step: {step}"
                    logger.error(error_msg)
                    return {
                        'success': False,
                        'message': error_msg,
                        'details': {
                            'completed_steps': completed_steps,
                            'failed_step': step,
                            'mock_mode': True
                        }
                    }
                
                completed_steps.append(step)
            
            # Update mock device state
            self._update_mock_state(interface_name, interface_ip, security_zone)
            
            # Create configuration record
            config_record = {
                'timestamp': datetime.now().isoformat(),
                'interface_name': interface_name,
                'interface_ip': interface_ip,
                'security_zone': security_zone,
                'status': 'success',
                'mock_mode': True
            }
            
            self.config_history.append(config_record)
            
            result = {
                'success': True,
                'message': 'Mock configuration completed successfully',
                'details': {
                    'interface': interface_name,
                    'ip_address': interface_ip,
                    'security_zone': security_zone,
                    'completed_steps': completed_steps,
                    'mock_mode': True,
                    'timestamp': datetime.now().isoformat(),
                    'simulated_commands': self._generate_mock_commands(
                        interface_name, interface_ip, security_zone
                    )
                }
            }
            
            logger.info("Mock configuration completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Mock configuration error: {str(e)}")
            return {
                'success': False,
                'message': f'Mock configuration failed: {str(e)}',
                'details': {'mock_mode': True}
            }
    
    def _update_mock_state(self, interface_name, interface_ip, security_zone):
        """Update internal mock device state"""
        
        # Update interface state
        if interface_name in self.interfaces:
            self.interfaces[interface_name].update({
                'status': 'up',
                'ip': interface_ip,
                'zone': security_zone,
                'description': 'Configured via automation'
            })
        
        # Update security zone
        if security_zone in self.security_zones:
            interface_unit = f"{interface_name}.0"
            if interface_unit not in self.security_zones[security_zone]['interfaces']:
                self.security_zones[security_zone]['interfaces'].append(interface_unit)
        
        # Add security policies
        http_policy = {
            'name': 'allow-http',
            'from_zone': 'trust',
            'to_zone': 'untrust',
            'source': 'any',
            'destination': 'any',
            'application': 'junos-http',
            'action': 'permit'
        }
        
        https_policy = {
            'name': 'allow-https',
            'from_zone': 'trust',
            'to_zone': 'untrust',
            'source': 'any',
            'destination': 'any',
            'application': 'junos-https',
            'action': 'permit'
        }
        
        self.security_policies.extend([http_policy, https_policy])
        
        logger.info("Mock device state updated")
    
    def _generate_mock_commands(self, interface_name, interface_ip, security_zone):
        """Generate mock Junos commands that would be applied"""
        
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
        
        return commands
    
    def get_interface_status(self):
        """Return current interface status"""
        return self.interfaces
    
    def get_security_zones(self):
        """Return security zone configuration"""
        return self.security_zones
    
    def get_security_policies(self):
        """Return security policies"""
        return self.security_policies
    
    def get_configuration_history(self):
        """Return configuration history"""
        return self.config_history
    
    def simulate_backup(self):
        """Simulate configuration backup"""
        logger.info("Creating mock configuration backup")
        
        time.sleep(1)  # Simulate backup time
        
        mock_config = {
            'timestamp': datetime.now().isoformat(),
            'device_info': self.get_device_info(),
            'interfaces': self.interfaces,
            'security_zones': self.security_zones,
            'security_policies': self.security_policies,
            'mock_mode': True
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'device_ip': 'mock-device',
            'configuration': json.dumps(mock_config, indent=2),
            'mock_mode': True
        }
    
    def simulate_rollback(self, rollback_id=1):
        """Simulate configuration rollback"""
        logger.info(f"Simulating rollback to configuration {rollback_id}")
        
        time.sleep(2)  # Simulate rollback time
        
        # Reset to default state (simplified rollback)
        if rollback_id == 1 and self.config_history:
            logger.info("Rolling back last configuration")
            self.config_history.pop()
        
        return {
            'success': True,
            'message': f'Mock rollback completed (rollback {rollback_id})',
            'details': {
                'rollback_id': rollback_id,
                'mock_mode': True,
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def simulate_connectivity_test(self, target_ip='8.8.8.8'):
        """Simulate network connectivity test"""
        logger.info(f"Simulating connectivity test to {target_ip}")
        
        time.sleep(1)  # Simulate ping time
        
        # Simulate 95% success rate
        success = random.random() > 0.05
        
        if success:
            return {
                'success': True,
                'target': target_ip,
                'packets_sent': 4,
                'packets_received': 4,
                'packet_loss': '0%',
                'avg_response_time': f"{random.uniform(1, 50):.1f}ms",
                'mock_mode': True
            }
        else:
            return {
                'success': False,
                'target': target_ip,
                'packets_sent': 4,
                'packets_received': 0,
                'packet_loss': '100%',
                'error': 'Request timeout (simulated)',
                'mock_mode': True
            }

# Standalone testing functionality
def main():
    """Test mock device functionality"""
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Mock SRX Device Simulator")
    print("=" * 40)
    
    mock_device = MockSRXDevice()
    
    # Test device info
    print("\n1. Device Information:")
    device_info = mock_device.get_device_info()
    for key, value in device_info.items():
        print(f"   {key}: {value}")
    
    # Test configuration
    print("\n2. Simulating Configuration:")
    result = mock_device.simulate_configuration(
        interface_name='ge-0/0/1',
        interface_ip='192.168.10.1/24',
        security_zone='trust'
    )
    
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    
    if result['success']:
        print("   Applied Commands:")
        for cmd in result['details']['simulated_commands']:
            print(f"     {cmd}")
    
    # Test backup
    print("\n3. Simulating Backup:")
    backup = mock_device.simulate_backup()
    print(f"   Backup created at: {backup['timestamp']}")
    
    # Test connectivity
    print("\n4. Simulating Connectivity Test:")
    connectivity = mock_device.simulate_connectivity_test()
    print(f"   Target: {connectivity['target']}")
    print(f"   Success: {connectivity['success']}")
    
    print("\nMock device testing completed!")

if __name__ == '__main__':
    main()
