# Juniper SRX Firewall Configuration Automation

## Overview

This is a web-based automation tool for configuring Juniper SRX firewalls using the Junos PyEZ library. The application provides both real device connectivity and mock simulation capabilities, making it suitable for development, testing, and production environments. It features a Flask web interface with REST API endpoints, allowing users to configure network interfaces, security zones, and firewall policies through an intuitive dashboard.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Web Framework**: Flask-based web application serving HTML templates
- **UI Components**: Bootstrap 5 for responsive design with Font Awesome icons
- **Client-side Logic**: Vanilla JavaScript for API interactions and dynamic UI updates
- **Template Engine**: Jinja2 templates for server-side rendering
- **Static Assets**: CSS and JavaScript files organized in standard Flask structure

### Backend Architecture
- **Application Server**: Flask web framework with RESTful API endpoints
- **Configuration Engine**: Custom SRXConfigurator class wrapping Junos PyEZ library
- **Mock Simulation**: MockSRXDevice class for testing without physical hardware
- **Error Handling**: Comprehensive exception handling with detailed logging
- **State Management**: In-memory configuration history tracking

### Device Communication
- **Protocol**: NETCONF over SSH for secure device communication
- **Library**: Junos PyEZ (junos-eznc) for native Juniper device interaction
- **Fallback Mode**: Mock device simulation when PyEZ is unavailable
- **Connection Management**: Persistent device connections with timeout handling

### Data Storage
- **Configuration History**: In-memory storage using Python lists/dictionaries
- **Logging**: File-based logging to 'srx_automation.log' with configurable levels
- **Session Management**: Flask built-in session handling with configurable secret key

### Security Features
- **Authentication**: SSH-based authentication for device connections
- **Session Security**: Flask secret key for session management
- **Input Validation**: Form validation and sanitization on both client and server side
- **Configuration Backup**: Automatic backup creation before applying changes

## External Dependencies

### Core Libraries
- **junos-eznc**: Juniper Networks PyEZ library for NETCONF device management
- **Flask**: Web framework for HTTP server and API endpoints
- **logging**: Python standard library for application logging

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN for responsive UI components
- **Font Awesome 6**: Icon library loaded via CDN for visual elements
- **Vanilla JavaScript**: No additional frontend frameworks, using native browser APIs

### Network Protocols
- **NETCONF**: Primary protocol for device configuration and management
- **SSH**: Secure transport layer for NETCONF communications (default port 22)
- **HTTP/HTTPS**: Web interface communication protocol

### Development Dependencies
- **Python 3**: Runtime environment with standard library modules
- **XML/ElementTree**: Built-in XML parsing for NETCONF responses
- **JSON**: Native JSON handling for API requests/responses

### Optional Components
- **Database Integration**: None currently implemented, but architecture supports future database integration
- **External APIs**: None currently integrated, but RESTful design allows for easy extension