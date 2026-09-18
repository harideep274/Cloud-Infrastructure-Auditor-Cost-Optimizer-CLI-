from google.auth import default
from google.cloud import compute_v1


def credentials():
    """Load Google Application Default Credentials."""
    creds, project = default()
    if not project:
        raise RuntimeError(
            "No Google Cloud project found. "
            "Set GOOGLE_CLOUD_PROJECT or configure gcloud."
        )
    return creds, project


def compute_client():
    """Create a Google Compute Engine client."""
    creds, _ = credentials()
    return compute_v1.InstancesClient(credentials=creds)


def project_id():
    """Return the active Google Cloud project ID."""
    _, project = credentials()
    return project
