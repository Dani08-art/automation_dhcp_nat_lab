# automation_dhcp_nat_lab

Python-driven network automation lab built on EVE-NG with Cisco IOL devices. After manually configuring only the base IPs and SSH access on each router, Python took over — automatically deploying centralized DHCP across 4 VLANs, pushing ip helper-address to distribution routers, configuring NAT/PAT for internet access, and backing up every router's running-config with a single script execution. No manual CLI for the complex part.

---

## Topology

```
                    [R4-ISP]
                    200.0.0.2
                        |
                    200.0.0.1
                    [R1-CORE]
                192.168.80.100 (Management)
                /                         \
          10.0.12.2                   10.0.13.2
          [R2-LEFT]                   [R3-RIGHT]
          /        \                  /         \
    e0/1.10      e0/1.20        e0/1.30       e0/1.40
    VLAN10       VLAN20         VLAN30        VLAN40
       |            |              |             |
   [SW-LEFT]    [SW-LEFT]      [SW-RIGHT]   [SW-RIGHT]
   Ventas       RRHH           IT           MGMT
```

---

## Network Design

### Point-to-Point Links (/30)

| Link | Side A | Side B |
|------|--------|--------|
| R1 ↔ R2 | 10.0.12.1/30 | 10.0.12.2/30 |
| R1 ↔ R3 | 10.0.13.1/30 | 10.0.13.2/30 |
| R1 ↔ ISP | 200.0.0.1/30 | 200.0.0.2/30 |

### VLANs

| VLAN | Name | Network | Gateway |
|------|------|---------|---------|
| 10 | Ventas | 10.10.0.0/24 | 10.10.0.1 |
| 20 | RRHH | 10.20.0.0/24 | 10.20.0.1 |
| 30 | IT | 10.30.0.0/24 | 10.30.0.1 |
| 40 | MGMT | 10.40.0.0/24 | 10.40.0.1 |
| 90 | GESTION | 10.0.21.0/30 | Management |
| 999 | NATIVE | — | Trunk security |

### Management

| Device | IP |
|--------|----|
| R1-CORE | 192.168.80.100 |
| R2-LEFT | 10.0.12.2 |
| R3-RIGHT | 10.0.13.2 |

---

## Protocols Configured

- **OSPF** — dynamic routing across R1, R2, R3 with loopbacks as Router-IDs
- **Router on a Stick** — Inter-VLAN routing via dot1Q subinterfaces on R2 and R3
- **DHCP** — centralized on R1 with `ip helper-address` on R2 and R3
- **NAT/PAT** — all VLANs translated to R1's public IP (200.0.0.1)
- **SSH v2** — enabled on all routers for remote management
- **Native VLAN 999** — applied on all trunks for security

---

## Python Automation

### Requirements

```bash
pip install netmiko
```

### Scripts

#### `dhcp_nat.py`
Configures centralized DHCP pools on R1 and pushes `ip helper-address` to R2 and R3.

```python
from netmiko import ConnectHandler

# Connects to R1, R2, R3
# Pushes DHCP pools for VLAN10, 20, 30, 40
# Configures ip helper-address pointing to R1 loopback (1.1.1.1)
```

#### `amg_nat.py`
Deploys NAT/PAT on R1.

```python
# Creates ACL-NAT permitting all internal VLANs
# Sets ip nat inside on internal interfaces
# Sets ip nat outside on ISP-facing interface
# Enables PAT with overload
```

#### `amg_backup.py`
Backs up running-config from all routers automatically.

```python
# Connects to each router
# Executes show running-config
# Saves output as hostname_YYYY-MM-DD.txt in /backups folder
```

---

## Project Structure

```
automation_dhcp_nat_lab/
├── dhcp_nat.py          # DHCP + helper-address automation
├── amg_nat.py           # NAT/PAT automation
├── amg_backup.py        # Automated config backup
├── backups/             # Router configs saved here
│   ├── R1_2026-04-08.txt
│   ├── R2-LEFT_2026-04-08.txt
│   └── R3-RIGHT_2026-04-08.txt
└── README.md
```

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Dani08-art/automation_dhcp_nat_lab

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install netmiko

# 4. Run scripts
python dhcp_nat.py
python amg_nat.py
python amg_backup.py
```

---

## Key Troubleshooting

**Netmiko ReadTimeout on ACL config**
Netmiko loses the prompt inside `config-std-nacl` mode. Fixed by splitting ACL commands and interface commands into separate `send_config_set()` calls.

**DHCP not reaching clients**
Missing `ip helper-address` on subinterfaces and incorrect subinterface encapsulation on R2/R3. Fixed by verifying dot1Q encapsulation matched VLAN IDs on both router and switch trunk.

**L2 switch connectivity**
L2 switches are not directly managed via SSH — connectivity validated end-to-end by confirming DHCP assignment and ping reachability from all VLAN clients (Ventas, RRHH, IT, MGMT) through their respective gateways.

---

## Author

**Daniel Vargas** — Network Engineer  
[LinkedIn](https://linkedin.com/in/daniel-vargas-644ab820a) | [GitHub](https://github.com/Dani08-art)
