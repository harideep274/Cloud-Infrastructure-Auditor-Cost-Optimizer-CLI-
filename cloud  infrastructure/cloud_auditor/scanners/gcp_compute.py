from . import __init__  # noqa: F401

from ..models import Finding
from ..gcp import compute_client, project_id


def scan():
    """Scan GCP Compute Engine VM instances."""
    client = compute_client()
    project = project_id()
    findings = []

    for zone in client.aggregated_list(
        request={"project": project}
    ):
        zone_name, response = zone

        if not response:
            continue

        for instance in response.instances:
            if instance.status != "RUNNING":
                continue

            findings.append(
                Finding(
                    provider="gcp",
                    account=project,
                    region=zone_name,
                    resource_type="Compute Engine VM",
                    resource_id=instance.name,
                    issue="Running GCP VM detected",
                    severity="info",
                    estimated_monthly_savings=0.0,
                    recommendation=(
                        "Review utilization and consider "
                        "rightsizing or scheduling this VM."
                    ),
                    metadata={
                        "machine_type": instance.machine_type,
                        "status": instance.status,
                    },
                )
            )

    return findings
