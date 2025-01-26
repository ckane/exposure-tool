class PasswordTester(object):
    """Defines the Password policy across the environment"""
    def test_password_strength(pw):
        # Passwords must not contain the word "weak"
        if pw.find("weak") >= 0:
            return [{"type": "access", "message": f"Password \"{pw}\" fails password strength test"}]

        return []

    def test_password(pw):
        # This function acts as a means to test password strength / adherence to policy
        # also could be used to look up passwords in a known exposed list like rockyou.txt
        defects = []

        # Simulate these tests:
        exposed_list = ["anotherweakpassword"]
        if pw in exposed_list:
            defects.append({"type": "access", "message": f"Password \"{pw}\" found in exposed db"})
        defects.extend(PasswordTester.test_password_strength(pw))

        return defects

class VirtualMachinePolicy(object):
    """Defines the VirtualMachine policy across the environment"""
    def validate(infra):
        defects = []

        # Test password if provided in VM information
        if 'password' in infra:
            defects.extend(PasswordTester.test_password(infra['password']))

        # Test for allowed open ports
        # TODO: Scan services listening on ports and capture version info, determine if port 80 is
        # simply redirecting to 443 (an allowed mitigation), etc...
        if 'open_ports' in infra:
            # Policy permits 22 and 443 for VMs
            # Can add additional ports here if desired
            allowed_ports = [22, 443]
            for port in infra['open_ports']:
                if port not in allowed_ports:
                    defects.append({'type': 'access', 'message': f"Port {port} is not allowed to be open"})

        if 'encryption' in infra and not infra['encryption']:
            defects.append({'type': 'confidentiality', 'message': f"Encryption is not enabled, but policy says it should be"})

        if 'mfa_enabled' in infra and not infra['mfa_enabled']:
            defects.append({'type': 'confidentiality', 'message': f"MFA is not enabled, but policy says it should be"})

        return defects

class StorageAccountPolicy(object):
    """Defines the StorageAccount policy across the environment"""
    def validate(infra):
        defects = []

        # Storage accounts require encryption to be enabled
        if 'encryption' in infra and not infra['encryption']:
            defects.append({'type': 'confidentiality', 'message': f"Encryption is not enabled, but policy says it should be"})

        # For our critical infrastructure, policy prefers GRS to LRS storage
        if 'azure_specific' in infra and 'replication' in infra['azure_specific']:
            if infra['azure_specific']['replication'] != "GRS":
                defects.append({'type': 'availability', 'message': "It is recommended to use Global-Replication for higher availability"})

        return defects

class DatabasePolicy(object):
    """Defines the Database policy across the environment"""
    def validate(infra):
        defects = []

        # Test password if provided in VM information
        if 'password' in infra:
            defects.extend(PasswordTester.test_password(infra['password']))

        # Test for allowed open ports
        # In this case, we only allow 1433 (SQL Server), 3306 (MySQL), and 5432 (PostgreSQL)
        # these are ports permitted to be open on the VM so that other services can communicate with them,
        # but network access control should still restrict DB access to the systems/users it is serving
        if 'open_ports' in infra:
            allowed_ports = [1433, 3306, 5432]
            for port in infra['open_ports']:
                if port not in allowed_ports:
                    defects.append({'type': 'access', 'message': f"Port {port} is not allowed to be open"})

        if 'encryption' in infra and not infra['encryption']:
            defects.append({'type': 'confidentiality', 'message': f"Encryption is not enabled, but policy says it should be"})

        if 'mfa_enabled' in infra and not infra['mfa_enabled']:
            defects.append({'type': 'confidentiality', 'message': f"MFA is not enabled, but policy says it should be"})

        return defects

# Map the supported infrastructure types to their respective Policy classes
supported_infra = {
    'virtual_machine': VirtualMachinePolicy,
    'storage_account': StorageAccountPolicy,
    'database': DatabasePolicy,
}

def validate_policy(infra):
    # Simple if-statement to walk across the supported infrastructure types
    if infra['type'] not in supported_infra:
        return None

    # Call the appropriate validation function based on type of infrastructure
    policy = supported_infra[infra['type']]
    return policy.validate(infra)

