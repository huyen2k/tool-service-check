#!/usr/bin/env python3

import subprocess
import argparse
import datetime
import sys


def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


def log(logfile, msg):
    print(msg)
    logfile.write(msg + "\n")


def section(logfile, title):
    log(logfile, "\n" + "="*85)
    log(logfile, title)
    log(logfile, "="*85)

# =========================
# CHECK FUNCTIONS
# =========================


def check_service(service):
    output = run_cmd(f"sudo systemctl status {service}")
    return "Active: active (running)" in output, output


def check_port(port, protocol):
    if protocol.lower() == "tcp":
        cmd = f"ss -lntp | grep :{port}"
    else:
        cmd = f"ss -lnup | grep :{port}"
    output = run_cmd(cmd)
    return bool(output.strip()), output


def check_ufw(port, protocol):
    output = run_cmd("sudo ufw status verbose")
    if "inactive" in output.lower():
        return True, output
    rule = f"{port}/{protocol.lower()}"
    if rule in output and "ALLOW" in output:
        return True, output
    return False, output


def check_ping(target):
    output = run_cmd(f"ping -c 3 {target}")
    return "0% packet loss" in output, output

# =========================
# DIAGNOSTIC ENGINE
# =========================


def analyze(results):
    service_ok = results["service"]
    port_ok = results["port"]
    ufw_ok = results["ufw"]
    wan_ok = results["wan"]
    internet_ok = results["internet"]

    if not service_ok:
        return "CRITICAL: Service is not running.", \
               "Start the service using: sudo systemctl start <service>"

    if service_ok and not port_ok:
        return "ERROR: Service running but port not listening.", \
               "Check bind address or service configuration."

    if service_ok and port_ok and not ufw_ok:
        return "ERROR: Local firewall (UFW) blocking the port.", \
               "Run: sudo ufw allow <port>/<protocol>"

    if service_ok and port_ok and ufw_ok and not wan_ok:
        return "ERROR: Cannot reach Firewall WAN interface.", \
               "Check routing table and pfSense rules."

    if service_ok and port_ok and ufw_ok and wan_ok and not internet_ok:
        return "WARNING: No Internet connectivity.", \
               "Check pfSense outbound NAT or WAN gateway."

    if all([service_ok, port_ok, ufw_ok, wan_ok, internet_ok]):
        return "SUCCESS: All checks passed.", \
               "Environment appears healthy."

    return "UNKNOWN STATE", "Manual investigation required."

# =========================
# MAIN
# =========================


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Service Diagnostic Tool")

    parser.add_argument("--service", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--protocol", required=True)
    parser.add_argument("--wan-ip", required=True)

    args = parser.parse_args()

    logfile_name = f"service_diagnostic_pro_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    with open(logfile_name, "w") as logfile:

        section(logfile, "ADVANCED SERVICE DIAGNOSTIC REPORT")

        # Perform checks
        service_ok, service_output = check_service(args.service)
        port_ok, port_output = check_port(args.port, args.protocol)
        ufw_ok, ufw_output = check_ufw(args.port, args.protocol)
        wan_ok, wan_output = check_ping(args.wan_ip)
        internet_ok, internet_output = check_ping("8.8.8.8")

        # Log raw outputs
        section(logfile, "RAW CHECK OUTPUTS")

        log(logfile, "[Service Status]")
        log(logfile, service_output)

        log(logfile, "[Port Check]")
        log(logfile, port_output)

        log(logfile, "[UFW Status]")
        log(logfile, ufw_output)

        log(logfile, "[WAN Ping]")
        log(logfile, wan_output)

        log(logfile, "[Internet Ping]")
        log(logfile, internet_output)

        # Analysis
        section(logfile, "AUTOMATED DIAGNOSTIC RESULT")

        results = {
            "service": service_ok,
            "port": port_ok,
            "ufw": ufw_ok,
            "wan": wan_ok,
            "internet": internet_ok
        }

        diagnosis, recommendation = analyze(results)

        log(logfile, f"Diagnosis      : {diagnosis}")
        log(logfile, f"Recommendation : {recommendation}")

    print(f"\nDetailed report saved to: {logfile_name}")


if __name__ == "__main__":
    main()
