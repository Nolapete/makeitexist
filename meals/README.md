# Meal Suggestions

## Project Overview

**Meal Suggestions** is a web application designed to help users plan their meals and manage recipes efficiently. Built with Django, this project provides a functional and user-friendly platform for adding, editing, and discovering meal ideas. The application features user authentication, ingredient management, and a dynamic meal suggestion algorithm.

## Accomplishments

### Core Application Structure
*   **Django Project Setup:** The project was built on the Django web framework, with a structured project (`mealSuggestions`) and app (`recipes`) layout.
*   **Database Models:** The application's data is managed through three core models: `Recipe`, `Ingredient`, and `MealLog`, defining relationships for users, recipes, and ingredients.
*   **URL Routing:** A robust URL configuration was established, handling routes for the admin interface, user authentication, and all application features.
*   **Database Migrations:** The project includes a history of database schema changes, including a successful transition from a complex `through` model to a simpler `ManyToManyField` for ingredients.

### User and Recipe Management
*   **User Authentication:** Implemented Django's built-in authentication for secure user logins, logouts, and access control via the `@login_required` decorator.
*   **Recipe Creation (`add_recipe`):** Users can add new recipes, including a title, description, instructions, and ingredients.
*   **Recipe Editing (`edit_recipe`):** A dedicated view and template allow the recipe's owner to update recipe details and ingredients.
*   **Recipe Viewing (`recipe_detail`):** Displays comprehensive information for a single recipe, including ingredients and a log of past selections.
*   **Recipe Listing (`my_recipes`):** Users can view a list of all recipes they have created.

### Ingredient and Meal Management
*   **Ingredient Management:** Users can add new ingredients via a dedicated form. The form now remains on the same page after submission, providing user-friendly feedback.
*   **Dynamic Ingredient Selection:** The recipe creation and editing pages feature a JavaScript-powered dual-listbox for managing ingredients. This functionality mimics the Django admin's user interface, offering a modern, responsive user experience.
*   **Meal Suggestions:** An algorithm suggests up to three recipes, prioritizing those not chosen in the last 30 days.
*   **Meal Logging (`choose_meal`):** Users can log when they choose a meal, which updates the `last_chosen` date on the recipe and creates an entry in the `MealLog`.

### Interface and User Experience
*   **Responsive UI:** The application uses a base template for consistent styling and a Flexbox layout for the dual-listbox ingredient selector, ensuring a responsive design.
*   **Dynamic Navigation:** The navigation bar is dynamic, showing links based on the user's authentication status and including links for adding recipes, adding ingredients, and viewing their recipes.
*   **User Feedback:** The application provides success messages to the user after actions like saving a new ingredient.

### Technical Achievements
*   **HTMX/JavaScript Integration:** Successfully transitioned from a server-heavy formset approach to a client-side JavaScript implementation for the dual-listbox ingredient selector.
*   **Error Resolution:** Addressed and resolved common Django errors such as `NoReverseMatch`, `TemplateDoesNotExist`, and `IntegrityError`, demonstrating effective debugging and refactoring skills.

## Getting Started

### Prerequisites
*   Python 3.x
*   Django

### Installation
1.  Clone the repository:
    ```sh
    git clone https://github.com/your-username/mealSuggestions.git
    cd mealSuggestions
    ```

2.  Set up a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  Install dependencies:
    ```sh
    pip install Django
    ```

4.  Set up the database:
    ```sh
    python manage.py makemigrations recipes
    python manage.py migrate
    ```

5.  Create a superuser to access the admin panel:
    ```sh
    python manage.py createsuperuser
    ```

6.  Start the development server:
    ```sh
    python manage.py runserver
    ```

7.  Navigate to `http://127.0.0.1:8000/` in your browser to view the application.

