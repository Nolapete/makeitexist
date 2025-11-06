# ruff: noqa: S101, W0621, S106
# tickets/tests/test_forms.py

from tickets.forms import TicketForm


def test_form_fields():
    """Test that the form contains the expected fields."""
    form = TicketForm()
    expected_fields = ["title", "description", "priority"]
    assert list(form.fields.keys()) == expected_fields


def test_form_valid_data():
    """Test that the form is valid with correct data."""
    form_data = {
        "title": "A valid title",
        "description": "A valid description for the ticket.",
        "priority": "high",
    }
    form = TicketForm(data=form_data)
    assert form.is_valid() is True


def test_form_invalid_missing_title():
    """Test that the form is invalid when the title is missing."""
    form_data = {
        "description": "Missing title should cause an error.",
        "priority": "medium",
    }
    form = TicketForm(data=form_data)
    assert form.is_valid() is False
    assert "title" in form.errors


def test_form_invalid_priority_choice():
    """Test that the form is invalid when an invalid priority is provided."""
    form_data = {
        "title": "Title",
        "description": "Invalid priority test.",
        "priority": "super_high",  # Invalid choice
    }
    form = TicketForm(data=form_data)
    assert form.is_valid() is False
    assert "priority" in form.errors


def test_form_widgets_have_tailwind_classes():
    """Test that the specified widgets have the correct Tailwind CSS classes."""
    form = TicketForm()

    # Define a core set of Tailwind classes you expect to be present on all fields
    # We will check for one representative class as a simple assertion
    expected_representative_class = "block"

    # Check title widget
    title_classes = form.fields["title"].widget.attrs.get("class", "")
    assert expected_representative_class in title_classes
    assert "border-gray-300" in title_classes  # Another specific check

    # Check description widget
    description_classes = form.fields["description"].widget.attrs.get("class", "")
    assert expected_representative_class in description_classes
    assert (
        "rows" in form.fields["description"].widget.attrs
    )  # Ensure 'rows' attribute is present

    # Check priority widget
    priority_classes = form.fields["priority"].widget.attrs.get("class", "")
    assert expected_representative_class in priority_classes
