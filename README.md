# Network CI/CD

## Pytest tasks

### using get_facts

- Check hostname is correct

### using get_interfaces

- Check all interfaces are in up/up state
- Check interface description matches topology

### using get_interfaces_ip

- Check own ip addresses are correct

### using get_bgp_neighbors

- Check BGP neighbors are established
- Check BGP ASN is correct

### using get_route_to

- Check expected routes are present
- Check unexpected routes are not present

### using ping

- Check reachability to all fabric devices
