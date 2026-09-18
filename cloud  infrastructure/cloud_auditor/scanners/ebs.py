from ..models import Finding


def scan(
    sess,
    account,
    region
):
    ec2 = sess.client(
        "ec2",
        region_name=region
    )

    response = ec2.describe_volumes(
        Filters=[
            {
                "Name": "status",
                "Values": ["available"]
            }
        ]
    )

    findings = []

    for volume in response.get("Volumes", []):

        size = volume.get("Size", 0)

        volume_type = volume.get(
            "VolumeType",
            "gp2"
        )

        # Conservative estimate.
        # Actual AWS pricing varies by region.
        rate = 0.08

        estimated_savings = round(
            size * rate,
            2
        )

        finding = Finding(
            provider="aws",
            account=account,
            region=region,
            resource_type="EBS Volume",
            resource_id=volume["VolumeId"],
            issue="Unattached volume",
            severity="medium",
            estimated_monthly_savings=estimated_savings,
            recommendation=(
                "Snapshot and verify ownership, "
                "then delete if confirmed orphaned."
            ),
            metadata={
                "size_gib": size,
                "volume_type": volume_type
            }
        )

        findings.append(finding)

    return findings