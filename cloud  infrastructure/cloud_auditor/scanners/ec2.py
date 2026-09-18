from datetime import datetime, timedelta, timezone

from ..models import Finding


def scan(
    sess,
    account,
    region,
    days=14,
    cpu_threshold=5.0
):
    ec2 = sess.client(
        "ec2",
        region_name=region
    )

    cloudwatch = sess.client(
        "cloudwatch",
        region_name=region
    )

    end_time = datetime.now(
        timezone.utc
    )

    start_time = (
        end_time -
        timedelta(days=days)
    )

    instances = []

    paginator = ec2.get_paginator(
        "describe_instances"
    )

    pages = paginator.paginate(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )

    for page in pages:

        for reservation in page.get(
            "Reservations",
            []
        ):

            instances.extend(
                reservation.get(
                    "Instances",
                    []
                )
            )

    findings = []

    for instance in instances:

        instance_id = instance[
            "InstanceId"
        ]

        response = cloudwatch.get_metric_statistics(

            Namespace="AWS/EC2",

            MetricName="CPUUtilization",

            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id
                }
            ],

            StartTime=start_time,

            EndTime=end_time,

            Period=3600,

            Statistics=[
                "Average"
            ]
        )

        datapoints = response.get(
            "Datapoints",
            []
        )

        cpu_values = [
            point["Average"]
            for point in datapoints
        ]

        if not cpu_values:
            continue

        average_cpu = (
            sum(cpu_values) /
            len(cpu_values)
        )

        if average_cpu < cpu_threshold:

            finding = Finding(

                provider="aws",

                account=account,

                region=region,

                resource_type="EC2 Instance",

                resource_id=instance_id,

                issue=(
                    f"Average CPU "
                    f"{average_cpu:.2f}% "
                    f"over {days} days"
                ),

                severity="high",

                estimated_monthly_savings=0.0,

                recommendation=(
                    "Rightsize, stop, or schedule "
                    "the instance after workload-owner "
                    "review."
                ),

                metadata={
                    "instance_type":
                        instance.get(
                            "InstanceType"
                        ),

                    "avg_cpu_percent":
                        round(
                            average_cpu,
                            2
                        ),

                    "datapoints":
                        len(cpu_values)
                }
            )

            findings.append(
                finding
            )

    return findings
