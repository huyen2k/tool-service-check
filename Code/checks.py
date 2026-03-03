#!/usr/bin/env python3
"""
Service diagnostic check functions
"""

from utils import run_cmd


class ServiceChecker:
    """Container for all diagnostic check functions"""

    @staticmethod
    def check_service(service):
        """
        Check if a service is running.

        Args:
            service (str): Service name

        Returns:
            tuple: (bool: service_is_running, str: command_output)
        """
        output = run_cmd(f"sudo systemctl status {service}")
        is_running = "Active: active (running)" in output
        return is_running, output

    @staticmethod
    def check_port(port, protocol):
        """
        Check if a port is listening.

        Args:
            port (int): Port number
            protocol (str): Protocol type (tcp/udp)

        Returns:
            tuple: (bool: port_is_listening, str: command_output)
        """
        if protocol.lower() == "tcp":
            cmd = f"ss -lntp | grep :{port}"
        else:
            cmd = f"ss -lnup | grep :{port}"

        output = run_cmd(cmd)
        is_listening = bool(output.strip())
        return is_listening, output

    @staticmethod
    def check_ufw(port, protocol):
        """
        Check if UFW (local firewall) allows the port.

        Args:
            port (int): Port number
            protocol (str): Protocol type (tcp/udp)

        Returns:
            tuple: (bool: port_is_allowed, str: command_output)
        """
        output = run_cmd("sudo ufw status verbose")

        # If UFW is inactive, it's not blocking
        if "inactive" in output.lower():
            return True, output

        # Check if rule exists and is ALLOW
        rule = f"{port}/{protocol.lower()}"
        is_allowed = rule in output and "ALLOW" in output

        return is_allowed, output

    @staticmethod
    def check_ping(target):
        """
        Check connectivity to a target IP.

        Args:
            target (str): Target IP address

        Returns:
            tuple: (bool: ping_successful, str: command_output)
        """
        output = run_cmd(f"ping -c 3 {target}")
        success = "0% packet loss" in output
        return success, output
