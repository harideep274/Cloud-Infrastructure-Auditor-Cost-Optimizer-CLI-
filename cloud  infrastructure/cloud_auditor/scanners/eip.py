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

    response = ec2.describe_addresses()

    findings = []

    for address in response.get(
        "Addresses",
        []
    ):

        # An Elastic IP without an association
        # is potentially unused.

        if not address.get(
            "AssociationId"
        ):

            allocation_id = address.get(
                "AllocationId",
                address.get(
                    "PublicIp",
                    "unknown"
                )
            )

            finding = Finding(
                provider="aws",
                account=account,
                region=region,
                resource_type="Elastic IP",
                resource_id=allocation_id,
                issue="Unassociated Elastic IP",
                severity="medium",

                # Policy estimate.
                estimated_monthly_savings=3.65,

                recommendation=(
                    "Release the Elastic IP after "
                    "confirming it is not required."
                ),

                metadata={
                    "public_ip": address.get(
                        "PublicIp"
                    )
                }
            )

            findings.append(finding)

    return findings
