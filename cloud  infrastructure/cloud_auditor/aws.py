import boto3

from botocore.config import Config


def session(
    profile: str | None = None,
    role_arn: str | None = None
):
    """
    Create an AWS boto3 session.

    Supports:
    - Default AWS credential chain
    - Named AWS profiles
    - Cross-account IAM role assumption
    """

    if profile:
        base_session = boto3.Session(
            profile_name=profile
        )
    else:
        base_session = boto3.Session()

    if not role_arn:
        return base_session

    sts = base_session.client(
        "sts",
        config=Config(
            retries={
                "max_attempts": 8,
                "mode": "adaptive"
            }
        )
    )

    credentials = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="cloud-auditor"
    )["Credentials"]

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )


def account_id(sess):
    """
    Return the AWS account ID.
    """

    sts = sess.client("sts")

    return sts.get_caller_identity()["Account"]


def regions(sess):
    """
    Return all enabled AWS regions.
    """

    ec2 = sess.client(
        "ec2",
        region_name="us-east-1"
    )

    response = ec2.describe_regions(
        AllRegions=False
    )

    return response["Regions"]


def client(
    sess,
    service,
    region
):
    """
    Create a boto3 client with adaptive retries.
    """

    return sess.client(
        service,
        region_name=region,
        config=Config(
            retries={
                "max_attempts": 8,
                "mode": "adaptive"
            }
        )
    )
