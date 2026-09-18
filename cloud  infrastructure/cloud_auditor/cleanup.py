from rich.console import Console


def plan(findings):
    """
    Select resources eligible for cleanup.

    EC2 is intentionally excluded because
    low CPU does not prove that termination
    is safe.
    """

    return [
        finding
        for finding in findings
        if finding.resource_type in (
            "EBS Volume",
            "Elastic IP"
        )
    ]


def execute(
    sess,
    findings,
    confirm=False
):
    """
    Execute destructive cleanup.

    Explicit confirmation is mandatory.
    """

    if not confirm:

        raise RuntimeError(
            "Refusing destructive execution "
            "without explicit confirmation."
        )

    deleted = []

    for finding in plan(findings):

        ec2 = sess.client(
            "ec2",
            region_name=finding.region
        )

        if (
            finding.resource_type ==
            "EBS Volume"
        ):

            ec2.delete_volume(
                VolumeId=finding.resource_id
            )

            deleted.append(
                finding.resource_id
            )

        elif (
            finding.resource_type ==
            "Elastic IP"
        ):

            ec2.release_address(
                AllocationId=finding.resource_id
            )

            deleted.append(
                finding.resource_id
            )

    Console().print(
        f"Deleted/released "
        f"{len(deleted)} resources."
    )

    return deleted
