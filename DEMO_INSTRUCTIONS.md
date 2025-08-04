# 🚀 SRX Automation Demo Instructions

## Quick Start for Your Internship Presentation

### Option 1: Web Interface Demo (Recommended)
1. **Open the web application** in your browser
2. **Keep "Mock/Simulation Mode" selected** (default)
3. **Click "Test Connection"** - shows device info
4. **Click "Apply Configuration"** - watch the progress
5. **View "Configuration Results"** - see applied commands
6. **Click "View Network Topology"** - show network diagram

### Option 2: Command Line Script Demo
```bash
# Run the standalone script
python standalone_script.py --mock

# Or with custom parameters
python standalone_script.py --mock --interface ge-0/0/2 --ip 10.1.1.1/24
```

## What Your Supervisor Will See

### 🎯 Professional Features:
- **Real-time progress tracking** during configuration
- **Detailed logging** of all operations  
- **Error handling** and recovery
- **Configuration backup** before changes
- **Network topology visualization**
- **Command history** and audit trail

### 💻 Technical Demonstration:
1. **Device Connection**: Shows authentication and connectivity
2. **Interface Configuration**: Assigns IP 192.168.10.1/24 to ge-0/0/1
3. **Security Zone Assignment**: Adds interface to trust zone
4. **Policy Creation**: Creates HTTP/HTTPS traffic policies
5. **Configuration Commit**: Applies changes safely

### 📊 Key Commands Generated:
```
set interfaces ge-0/0/1 unit 0 family inet address 192.168.10.1/24
set interfaces ge-0/0/1 unit 0 description 'Automated configuration'
set security zones security-zone trust interfaces ge-0/0/1.0
set security policies from-zone trust to-zone untrust policy allow-http match source-address any
set security policies from-zone trust to-zone untrust policy allow-http match destination-address any
set security policies from-zone trust to-zone untrust policy allow-http match application junos-http
set security policies from-zone trust to-zone untrust policy allow-http then permit
```

## 🎨 Network Topology for Draw.io

### Layout Description:
**Create this diagram in Draw.io:**

1. **Internet Cloud** (top center)
   - Blue cloud shape
   - Label: "Internet"

2. **Main SRX Firewall** (center)
   - Red firewall icon
   - Label: "SRX-Main (192.168.1.1)"
   - Interfaces: ge-0/0/0 (untrust), ge-0/0/1 (trust)

3. **Remote SRX Firewall** (left)
   - Red firewall icon  
   - Label: "SRX-Branch (10.0.0.1)"

4. **VPN Tunnel** (between SRX devices)
   - Dashed yellow line
   - Label: "IPsec VPN Tunnel"

5. **Trust Network** (right side)
   - Green dashed box around internal devices
   - Label: "Trust Zone (192.168.10.0/24)"
   - Switch connected to SRX ge-0/0/1
   - 2-3 workstations connected to switch

6. **Untrust Zone** (top)
   - Red dashed box around internet connection
   - Label: "Untrust Zone"

### Color Scheme:
- **Trust Zone**: Green (#28a745)
- **Untrust Zone**: Red (#dc3545)  
- **VPN Zone**: Yellow (#ffc107)
- **Devices**: Use standard network icons

## 🎤 Presentation Script

### Introduction (30 seconds):
"I've built a Python automation tool for Juniper SRX firewalls that demonstrates network automation principles used in enterprise environments."

### Demo Flow (2-3 minutes):
1. "This web interface connects to SRX devices using the Junos PyEZ library"
2. "Mock mode lets us demonstrate without physical hardware"
3. "Watch as it configures the interface, assigns security zones, and creates policies"
4. "The system shows real-time progress and logs all operations"
5. "Here's the network topology showing our automated configuration"

### Technical Highlights:
- "Uses industry-standard NETCONF protocol"
- "Includes error handling and rollback capabilities"  
- "Generates audit logs for compliance"
- "Supports both simulation and real device modes"

## 🔧 Troubleshooting

**If something doesn't work:**
1. Refresh the browser page
2. Make sure "Mock/Simulation Mode" is selected
3. Check that the server is running (should see green status)

**For questions about real devices:**
- Mention that this works with actual SRX hardware when available
- Mock mode demonstrates all the same functionality safely

## 📝 Project Summary for Documentation

**Technologies Used:**
- Python 3
- Flask web framework  
- Junos PyEZ library
- Bootstrap UI
- NETCONF protocol
- Mock simulation for testing

**Key Achievements:**
- Automated interface configuration
- Security zone management
- Policy creation and management
- Real-time monitoring
- Professional web interface
- Comprehensive error handling

Your project demonstrates real-world network automation skills that are highly valued in the industry!