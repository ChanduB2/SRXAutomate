#!/usr/bin/env python3
"""
Juniper SRX Firewall Configuration Automation Web Interface
A Flask web application for automating SRX firewall configuration
with mock simulation capabilities.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, flash
from datetime import datetime
import json

from srx_config import SRXConfigurator
from mock_device import MockSRXDevice

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('srx_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'srx-automation-key-2025')

# Global configuration storage
config_history = []

@app.route('/')
def index():
    """Main dashboard for SRX configuration automation"""
    return render_template('index.html')

@app.route('/topology')
def topology():
    """Network topology visualization page"""
    return render_template('topology.html')

@app.route('/api/configure', methods=['POST'])
def configure_device():
    """Configure SRX device via API"""
    try:
        data = request.get_json()
        
        # Extract configuration parameters
        device_ip = data.get('device_ip', '192.168.1.1')
        username = data.get('username', 'admin')
        password = data.get('password', 'admin')
        mock_mode = data.get('mock_mode', True)
        
        # Configuration parameters
        interface_name = data.get('interface_name', 'ge-0/0/1')
        interface_ip = data.get('interface_ip', '192.168.10.1/24')
        security_zone = data.get('security_zone', 'trust')
        
        logger.info(f"Starting configuration - Mock Mode: {mock_mode}")
        
        if mock_mode:
            # Use mock device simulation
            mock_device = MockSRXDevice()
            result = mock_device.simulate_configuration(
                interface_name=interface_name,
                interface_ip=interface_ip,
                security_zone=security_zone
            )
        else:
            # Use real device configuration
            configurator = SRXConfigurator(
                host=device_ip,
                user=username,
                password=password
            )
            
            result = configurator.configure_interface_and_policy(
                interface_name=interface_name,
                interface_ip=interface_ip,
                security_zone=security_zone
            )
        
        # Store configuration in history
        config_entry = {
            'timestamp': datetime.now().isoformat(),
            'device_ip': device_ip,
            'mock_mode': mock_mode,
            'interface_name': interface_name,
            'interface_ip': interface_ip,
            'security_zone': security_zone,
            'result': result
        }
        config_history.append(config_entry)
        
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', 'Configuration completed'),
            'details': result.get('details', {}),
            'config_id': len(config_history)
        })
        
    except Exception as e:
        logger.error(f"Configuration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Configuration failed: {str(e)}',
            'details': {}
        }), 500

@app.route('/api/status')
def device_status():
    """Get device connection status"""
    try:
        data = request.args
        device_ip = data.get('device_ip', '192.168.1.1')
        mock_mode = data.get('mock_mode', 'true').lower() == 'true'
        
        if mock_mode:
            # Mock device is always available
            return jsonify({
                'connected': True,
                'device_info': {
                    'model': 'vSRX (Mock)',
                    'version': '20.4R3.8 (Mock)',
                    'serial': 'VM123456789 (Mock)',
                    'uptime': '45 days, 12:34:56 (Mock)'
                },
                'interfaces': {
                    'ge-0/0/0': {'status': 'up', 'ip': '10.0.0.1/24'},
                    'ge-0/0/1': {'status': 'down', 'ip': 'unassigned'}
                }
            })
        else:
            # Try to connect to real device
            try:
                username = data.get('username', 'admin')
                password = data.get('password', 'admin')
                
                configurator = SRXConfigurator(
                    host=device_ip,
                    user=username,
                    password=password,
                    timeout=10
                )
                
                device_info = configurator.get_device_info()
                return jsonify({
                    'connected': True,
                    'device_info': device_info
                })
                
            except Exception as e:
                return jsonify({
                    'connected': False,
                    'error': str(e)
                })
                
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({
            'connected': False,
            'error': str(e)
        }), 500

@app.route('/api/history')
def configuration_history():
    """Get configuration history"""
    return jsonify({
        'history': config_history[-10:],  # Last 10 configurations
        'total': len(config_history)
    })

@app.route('/api/backup', methods=['POST'])
def backup_configuration():
    """Create configuration backup"""
    try:
        data = request.get_json()
        device_ip = data.get('device_ip', '192.168.1.1')
        mock_mode = data.get('mock_mode', True)
        
        if mock_mode:
            # Mock backup
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'device_ip': device_ip,
                'mock_mode': True,
                'configuration': 'Mock configuration backup data...'
            }
        else:
            # Real device backup
            username = data.get('username', 'admin')
            password = data.get('password', 'admin')
            
            configurator = SRXConfigurator(
                host=device_ip,
                user=username,
                password=password
            )
            
            backup_data = configurator.backup_configuration()
        
        return jsonify({
            'success': True,
            'backup': backup_data,
            'message': 'Configuration backup created successfully'
        })
        
    except Exception as e:
        logger.error(f"Backup error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Backup failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    logger.info("Starting SRX Automation Web Interface")
    logger.info("Access the application at http://localhost:5000")
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
