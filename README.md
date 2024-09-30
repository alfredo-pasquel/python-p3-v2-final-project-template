# Band Tour Manager CLI

This is a Python-based Command Line Interface (CLI) application for managing bands and scheduling their tour dates. The app allows users to create, view, update, and delete bands and tour dates, as well as view related information such as tour dates for a particular band.

## Features

- **Create, View, Update, and Delete Bands**: Manage band details including name and genre.
- **Schedule Tour Dates**: Schedule new tour dates for a band by specifying the location, venue, and date.
- **View Tour Dates**: Filter tour dates by band, location, or venue.
- **Update and Delete Tour Dates**: Modify or remove tour dates, with automatic validation to prevent double bookings.
- **Color-Coded Output**: Bands and tour dates are color-coded for better readability based on genre and location.

## Dependencies

The app uses several Python libraries to handle various aspects of functionality:

### 1. `colorama`
Used to color the terminal output, making it easier to differentiate between genres and locations when displaying bands and tour dates.

### 2. `tkcalendar`
Used for selecting dates in a graphical interface, allowing users to visually pick a date when scheduling or updating tour dates.

### 3. `sqlite3`
This app uses SQLite as its database to store bands and tour dates. SQLite is lightweight and doesn’t require a separate database server, making it ideal for this CLI application.

## How to Run the App

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install the required dependencies using `pipenv`
If you don’t have `pipenv` installed, first install it with:
```bash
pip install pipenv
```

Then, install the dependencies in a virtual environment:
```bash
pipenv install
```

### 3. Activate the virtual environment
Once the dependencies are installed, activate the virtual environment using:
```bash
pipenv shell
```

### 4. Run the app
To start the application, run:
```bash
python cli.py
```

### 5. Use the CLI
You’ll be presented with the main menu, from which you can navigate to the Bands or Tour Dates menus. Each menu provides options to create, view, update, and delete entries.

## Instructions for Use

### Band Management
- **Create a new band**: Enter the band name and genre.
- **View all bands**: Displays a list of all bands with color-coded genres.
- **Update a band**: Allows you to update the band’s name or genre.
- **Delete a band**: Permanently deletes a band from the database.

### Tour Date Management
- **Schedule a new tour date**: Allows you to select a band, set the location, venue, and pick a date from the calendar.
- **View all tour dates**: Filter by band, location, or venue.
- **Update a tour date**: Modify details of an existing tour date.
- **Delete a tour date**: Remove a tour date from the schedule.

## Example Output
Here’s what a typical interaction looks like:

```
Main Menu:
1. Bands Menu
2. Tour Dates Menu
> 1

Bands Menu:
1. Create a new band
2. View all bands
> 2

ID: 1, Name: metallica, Genre: heavy metal (color-coded)
```

## Future Improvements
- Add more robust error handling for edge cases.
- Implement more complex filtering and searching features for large datasets.
