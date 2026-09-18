from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from .aws import (
    account_id,
    regions
)

from .scanners import (
    ebs,
    eip,
    ec2,
    gcp_compute
)


def scan_aws(
    sess,
    include_ec2=True,
    days=14,
    cpu_threshold=5.0,
    max_workers=4
):
    """
    Execute AWS audit across enabled regions.
    """

    account = account_id(
        sess
    )

    region_data = regions(
        sess
    )

    aws_regions = [
        region["RegionName"]
        for region in region_data
    ]

    findings = []

    jobs = []

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        for region in aws_regions:

            jobs.append(
                executor.submit(
                    ebs.scan,
                    sess,
                    account,
                    region
                )
            )

            jobs.append(
                executor.submit(
                    eip.scan,
                    sess,
                    account,
                    region
                )
            )

            if include_ec2:

                jobs.append(
                    executor.submit(
                        ec2.scan,
                        sess,
                        account,
                        region,
                        days,
                        cpu_threshold
                    )
                )

        for job in as_completed(jobs):

            findings.extend(
                job.result()
            )

    return findings


def scan_gcp():
    """Execute GCP Compute Engine audit."""
    return gcp_compute.scan()
