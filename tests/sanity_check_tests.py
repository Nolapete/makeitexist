"""
Basic sanity checks to ensure pytest is configured and running correctly.
"""


def test_pytest_is_working():
    """
    A simple test that asserts True is True.

    This ensures that the test runner (pytest) is installed and functional
    in the environment where the pre-commit hook runs.
    """
    assert True is True, "This assertion should always pass if the test runs."


def test_project_name_exists():
    """
    Placeholder for future tests. This test ensures the tests directory isn't empty.
    """
    project_is_live = True
    assert project_is_live is True
