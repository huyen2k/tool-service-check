#!/usr/bin/env python3
"""
Diagnostic analysis engine for service checks
"""


class DiagnosticAnalyzer:
    """Analyze check results and provide diagnosis"""

    @staticmethod
    def analyze(results):
        """
        Analyze check results and provide diagnosis and recommendations.

        Args:
            results (dict): Dictionary containing check results:
                - service: bool - service is running
                - port: bool - port is listening
                - ufw: bool - UFW allows port
                - wan: bool - WAN IP is reachable
                - internet: bool - Internet is reachable

        Returns:
            tuple: (str: diagnosis, str: recommendation)
        """
        service_ok = results.get("service", False)
        port_ok = results.get("port", False)
        ufw_ok = results.get("ufw", False)
        wan_ok = results.get("wan", False)
        internet_ok = results.get("internet", False)

        # Flowchart: Check service first
        if not service_ok:
            return (
                "CRITICAL: Service is not running.",
                "Start the service using: sudo systemctl start <service>"
            )

        # Service is running but port not listening
        if service_ok and not port_ok:
            return (
                "ERROR: Service running but port not listening.",
                "Check bind address or service configuration."
            )

        # Service and port OK but UFW blocking
        if service_ok and port_ok and not ufw_ok:
            return (
                "ERROR: Local firewall (UFW) blocking the port.",
                "Run: sudo ufw allow <port>/<protocol>"
            )

        # Service, port, UFW OK but can't reach WAN
        if service_ok and port_ok and ufw_ok and not wan_ok:
            return (
                "ERROR: Cannot reach Firewall WAN interface.",
                "Check routing table and firewall (pfSense) rules."
            )

        # Service, port, UFW, WAN OK but no internet
        if service_ok and port_ok and ufw_ok and wan_ok and not internet_ok:
            return (
                "WARNING: No Internet connectivity.",
                "Check firewall outbound NAT or WAN gateway."
            )

        # All checks passed
        if all([service_ok, port_ok, ufw_ok, wan_ok, internet_ok]):
            return (
                "SUCCESS: All checks passed.",
                "Environment appears healthy. Service is accessible from internet."
            )

        # Unknown state
        return (
            "UNKNOWN STATE",
            "Manual investigation required. Check the detailed logs."
        )

    @staticmethod
    def get_status_summary(results):
        """
        Get a summary of all check statuses.

        Args:
            results (dict): Dictionary containing check results

        Returns:
            str: Formatted status summary
        """
        summary = []
        summary.append(
            f"  Service Running     : {'✓' if results.get('service') else '✗'}")
        summary.append(
            f"  Port Listening      : {'✓' if results.get('port') else '✗'}")
        summary.append(
            f"  UFW Allow           : {'✓' if results.get('ufw') else '✗'}")
        summary.append(
            f"  WAN Reachable       : {'✓' if results.get('wan') else '✗'}")
        summary.append(
            f"  Internet Connected  : {'✓' if results.get('internet') else '✗'}")
        return "\n".join(summary)
