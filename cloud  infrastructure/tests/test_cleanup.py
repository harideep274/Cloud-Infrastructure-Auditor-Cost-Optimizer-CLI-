import pytest

from cloud_auditor.cleanup import execute


def test_cleanup_requires_confirmation():

    with pytest.raises(
        RuntimeError
    ):

        execute(
            None,
            [],
            confirm=False
        )
        