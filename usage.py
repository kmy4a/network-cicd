from network_cicd.devices import factory

device = factory.create_device(os_type="eos", hostname="clab-clos-testbed-spine01", username="admin", password="admin")
interfaces = device.get_interfaces()
print("Interfaces:")
for ifname, info in interfaces.items():
    print(f"  {ifname}: {info}")

interfaces_ip = device.get_interfaces_ip()
print("\nInterface IPs:")
for ifname, ip_info in interfaces_ip.items():
    print(f"  {ifname}: {ip_info}")

bgp_neighbors = device.get_bgp_neighbors()
print("\nBGP Neighbors:")
for peer_ip, peer_info in bgp_neighbors["global"]["peers"].items():
    print(f"  {peer_ip}: {peer_info}")
routes = device.get_route_to(destination="10.0.0.0/8")

print("\nRoutes:")
for prefix, entries in routes.items():
    print(f"  {prefix}: {entries}")
