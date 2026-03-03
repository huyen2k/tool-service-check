#!/usr/bin/env python3
"""
Advanced Service Diagnostic Tool
A modular tool to check if a service is accessible from the internet.
"""

import argparse
import datetime
from checks import ServiceChecker
from logger import Logger
from analyzer import DiagnosticAnalyzer


class ServiceDiagnosticTool:
    """Main orchestrator for service diagnostic"""

    def __init__(self, service, port, protocol, wan_ip):
        """
        Initialize the diagnostic tool with parameters.

        Args:
            service (str): Service name
            port (int): Service port
            protocol (str): Protocol type (tcp/udp)
            wan_ip (str): WAN IP address for testing
        """
        self.service = service
        self.port = port
        self.protocol = protocol
        self.wan_ip = wan_ip
        self.checker = ServiceChecker()
        self.analyzer = DiagnosticAnalyzer()

    def perform_checks(self):
        """
        Execute all diagnostic checks.

        Returns:
            tuple: (results_dict, outputs_dict)
        """
        print(f"[*] Starting diagnostic checks for service: {self.service}")
        print(
            f"    Port: {self.port}, Protocol: {self.protocol}, WAN IP: {self.wan_ip}")
        print()

        # Perform all checks
        service_ok, service_output = self.checker.check_service(self.service)
        port_ok, port_output = self.checker.check_port(
            self.port, self.protocol)
        ufw_ok, ufw_output = self.checker.check_ufw(self.port, self.protocol)
        wan_ok, wan_output = self.checker.check_ping(self.wan_ip)
        internet_ok, internet_output = self.checker.check_ping("8.8.8.8")

        results = {
            "service": service_ok,
            "port": port_ok,
            "ufw": ufw_ok,
            "wan": wan_ok,
            "internet": internet_ok
        }

        outputs = {
            "service": service_output,
            "port": port_output,
            "ufw": ufw_output,
            "wan": wan_output,
            "internet": internet_output
        }

        return results, outputs

    def generate_report(self, results, outputs):
        """
        Generate a comprehensive diagnostic report.

        Args:
            results (dict): Check results
            outputs (dict): Raw command outputs

        Returns:
            str: Logfile name
        """
        logfile_name = f"service_diagnostic_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        with open(logfile_name, "w") as logfile:
            logger = Logger(logfile)

            # Header
            logger.section("ADVANCED SERVICE DIAGNOSTIC REPORT")
            logger.log(f"Service          : {self.service}")
            logger.log(f"Port             : {self.port}")
            logger.log(f"Protocol         : {self.protocol}")
            logger.log(f"WAN IP           : {self.wan_ip}")
            logger.log(
                f"Timestamp        : {datetime.datetime.now().isoformat()}")

            # Raw outputs
            logger.section("RAW CHECK OUTPUTS")
            logger.raw_output("Service Status", outputs["service"])
            logger.raw_output("Port Check", outputs["port"])
            logger.raw_output("UFW Status", outputs["ufw"])
            logger.raw_output("WAN Ping", outputs["wan"])
            logger.raw_output("Internet Ping", outputs["internet"])

            # Status summary
            logger.section("CHECK STATUS SUMMARY")
            logger.log(self.analyzer.get_status_summary(results))

            # Analysis
            logger.section("AUTOMATED DIAGNOSTIC RESULT")
            diagnosis, recommendation = self.analyzer.analyze(results)
            logger.result("Diagnosis", diagnosis)
            logger.result("Recommendation", recommendation)

        return logfile_name

    def run(self):
        """Execute the full diagnostic workflow"""
        results, outputs = self.perform_checks()
        logfile_name = self.generate_report(results, outputs)

        print(f"[✓] Detailed report saved to: {logfile_name}")

        # Print summary to console
        diagnosis, recommendation = self.analyzer.analyze(results)
        print(f"\n[DIAGNOSIS] {diagnosis}")
        print(f"[RECOMMENDATION] {recommendation}")


def main():
    """Parse arguments and run the diagnostic tool"""
    parser = argparse.ArgumentParser(
        description="Advanced Service Diagnostic Tool - Check if a service is accessible from the internet"
    )

    parser.add_argument(
        "--service",
        required=True,
        help="Service name (e.g., nginx, apache2, ssh)"
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="Service port number (e.g., 80, 443, 22)"
    )
    parser.add_argument(
        "--protocol",
        required=True,
        choices=["tcp", "udp"],
        help="Protocol type (tcp or udp)"
    )
    parser.add_argument(
        "--wan-ip",
        required=True,
        help="WAN IP address of the firewall"
    )

    args = parser.parse_args()

    # Create and run the diagnostic tool
    tool = ServiceDiagnosticTool(
        service=args.service,
        port=args.port,
        protocol=args.protocol,
        wan_ip=args.wan_ip
    )

    tool.run()


if __name__ == "__main__":
    main()
