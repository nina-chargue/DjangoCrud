#  The Task-Hive
A commerce app designed for auctions, where users can create profiles to either list items for auction or bid on others' listings. The app provides a dynamic and interactive platform for users to engage in buying and selling through auctions. Below is a detailed description of the features and functionalities of The Bazaar.

## [View the website](https://task-hive.azurewebsites.net/)

## Features

- User Authentication
  - Sign In and Register: Users can create a new account or sign in to an existing account to access the features of the app.
- User Profiles
  - Create Profile: Users can create and edit their profiles to personalize their experience.
- Tasks
  - Create Task: Users can create new task  by specifying a title, description, and marking it as important or not. The task will be shown under pending tasks.
  - Update Task: Clicking on a task will take the user to an edit interface where they can edit the task, delte it or mark it as completed.
  - Important: If a task is marked as important it will show in a different color. 
  
## Implementation

- **HTML**: Structured the web pages with HTML elements, including forms, input fields, buttons, and links.
- **CSS**: Styled the pages in a dark mode, using grey, orange and brown colors, rounded corners, and consistent button styling.
- **Python**: Used the Django framework for the backend.

## Development

This project was developed with Python, HTML and CSS. It served as a practical exercise to reinforce basic concepts of django. The app is deployed in azure web app service and has a postgres sql database.

## Usage

1. Clone the repository: git clone https://github.com/your_username/DjangoCrud.git
2. Navigate to the project directory.
3. Install dependencies: pip install -r requirements.txt
4. Run the Django application: python app.py / python managepy runserver
5. Change the database connection in the setting.py file to sqlite3. (Uncooment lines 88-89 and comment lines 91-97)
6. Open your web browser and go to http://localhost:5000 to start using the task-hive.

## Demonstrative Video 
https://www.youtube.com/watch?v=is8PS5UrMyY
