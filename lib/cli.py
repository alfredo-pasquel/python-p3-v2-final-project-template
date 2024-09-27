from colorama import Fore, init
from tkcalendar import Calendar
import tkinter as tk
from models.band import Band
from models.tour_date import TourDate
from helpers import exit_program
from datetime import datetime
import random

# Initialize colorama for CLI coloring
init(autoreset=True)

class ColorManager:
    COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW, Fore.WHITE]

    genre_colors = {}
    location_colors = {}
    
    # Sets to track used colors for genres and locations
    used_genre_colors = set()
    used_location_colors = set()

    @classmethod
    def get_genre_color(cls, genre):
        if genre not in cls.genre_colors:
            available_colors = [color for color in cls.COLORS if color not in cls.used_genre_colors]
            
            # If no available colors, reset the used colors
            if not available_colors:
                cls.used_genre_colors.clear()
                available_colors = cls.COLORS.copy()

            # Assign a random color from the available colors
            selected_color = random.choice(available_colors)
            cls.genre_colors[genre] = selected_color
            cls.used_genre_colors.add(selected_color)

        return cls.genre_colors[genre]

    @classmethod
    def get_location_color(cls, location):
        if location not in cls.location_colors:
            available_colors = [color for color in cls.COLORS if color not in cls.used_location_colors]
            
            # If no available colors, reset the used colors
            if not available_colors:
                cls.used_location_colors.clear()
                available_colors = cls.COLORS.copy()

            # Assign a random color from the available colors
            selected_color = random.choice(available_colors)
            cls.location_colors[location] = selected_color
            cls.used_location_colors.add(selected_color)

        return cls.location_colors[location]

# Function to select a date using tkcalendar
def select_date_gui():
    selected_date = None
    
    # Create the window
    root = tk.Tk()
    root.title("Select a Date")

    # Create the calendar widget
    cal = Calendar(root, selectmode='day', year=2024, month=10, day=1)
    cal.pack(pady=20)

    # Define a function to grab the selected date and destroy the window
    def grab_date():
        nonlocal selected_date
        selected_date = cal.get_date()
        root.quit()

    # Add a button to select the date
    select_btn = tk.Button(root, text="Select", command=grab_date)
    select_btn.pack(pady=20)

    # Start the main event loop
    root.mainloop()
    root.destroy()
    
    return selected_date

def validate_future_date(selected_date):
    # Convert selected date (in YYYY-MM-DD format) to a date object
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
    
    # Get the current date
    current_date = datetime.now().date()
    
    # Check if the selected date is in the future
    return selected_date_obj >= current_date

def format_date(date_str):
    try:
        # First, try converting from MM/DD/YY (tkcalendar format)
        formatted_date = datetime.strptime(date_str, "%m/%d/%y").strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        try:
            # If that fails, try converting from YYYY-MM-DD (manual entry format)
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            return formatted_date
        except ValueError as e:
            # Print the error and the problematic date
            print(f"Error formatting date: {date_str}")
            print(f"Exception: {e}")
            raise e  # Re-raise the error to avoid silent failures

def main():
    while True:
        print(Fore.BLUE + "Main Menu:")
        print(Fore.CYAN + "0. Exit Program")
        print(Fore.CYAN + "1. Bands Menu")
        print(Fore.CYAN + "2. Tour Dates Menu")
        choice = input(Fore.YELLOW + "> ")

        if choice == "0":
            exit_program()
        elif choice == "1":
            bands_menu()
        elif choice == "2":
            tour_dates_menu()
        else:
            print(Fore.RED + "Invalid choice")

def bands_menu():
    while True:
        print(Fore.BLUE + "Bands Menu:")
        print(Fore.CYAN + "0. Return to Main Menu")
        print(Fore.CYAN + "1. Create a new band")
        print(Fore.CYAN + "2. View all bands")
        print(Fore.CYAN + "3. Update a band")
        print(Fore.CYAN + "4. Delete a band")
        print(Fore.CYAN + "5. View related tour dates")
        choice = input(Fore.YELLOW + "> ")

        if choice == "0":
            break
        elif choice == "1":
            create_band()
        elif choice == "2":
            view_bands()
        elif choice == "3":
            update_band()
        elif choice == "4":
            delete_band()
        elif choice == "5":
            view_band_related_tours()
        else:
            print(Fore.RED + "Invalid choice")

def tour_dates_menu():
    while True:
        print(Fore.BLUE + "Tour Dates Menu:")
        print(Fore.CYAN + "0. Return to Main Menu")
        print(Fore.CYAN + "1. Schedule a new tour date")
        print(Fore.CYAN + "2. View all tour dates")
        print(Fore.CYAN + "3. Update a tour date")
        print(Fore.CYAN + "4. Delete a tour date")
        print(Fore.CYAN + "5. View related band")
        choice = input(Fore.YELLOW + "> ")

        if choice == "0":
            break
        elif choice == "1":
            schedule_tour_date()
        elif choice == "2":
            view_tour_dates()
        elif choice == "3":
            update_tour_date()
        elif choice == "4":
            delete_tour_date()
        elif choice == "5":
            view_tour_related_band()
        else:
            print(Fore.RED + "Invalid choice")

def view_bands():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID to view (leave blank to view all): ")

    if band_name_or_id:
        # Find by ID or name
        if band_name_or_id.isdigit():
            band = Band.find_by_id(band_name_or_id)
        else:
            band = Band.find_by_name(band_name_or_id)

        if not band:
            print(Fore.RED + "Band not found.")
        else:
            # Apply genre-based color randomization
            genre_color = ColorManager.get_genre_color(band[2])  
            print(genre_color + f"ID: {band[0]}, Name: {band[1]}, Genre: {band[2]}")
    else:
        # Display all bands
        bands = Band.all()
        for band in bands:
            # Apply genre-based color randomization
            genre_color = ColorManager.get_genre_color(band[2])
            print(genre_color + f"ID: {band[0]}, Name: {band[1]}, Genre: {band[2]}")

def create_band():
    name = input(Fore.CYAN + "Enter band name (max 50 characters): ")
    
    existing_band = Band.find_by_name(name)

    if existing_band:
        print(Fore.RED + f"Error: A band named '{name}' already exists.")
        return
    
    genre = input(Fore.CYAN + "Enter genre (max 30 characters): ")
    
    try:
        Band.create(name, genre)
        print(Fore.GREEN + f"Band '{name}' created.")
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def update_band():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID to update: ")

    # Find the band by name or ID
    if band_name_or_id.isdigit():
        band = Band.find_by_id(band_name_or_id)
    else:
        band = Band.find_by_name(band_name_or_id)

    if not band:
        print(Fore.RED + "Error: Band not found.")
        return

    new_name = input(Fore.CYAN + f"Enter new name for band '{band[1]}' (leave blank to keep current): ")
    new_genre = input(Fore.CYAN + f"Enter new genre for band '{band[2]}' (leave blank to keep current): ")

    try:
        Band.update(band[0], new_name if new_name else None, new_genre if new_genre else None)
        print(Fore.GREEN + f"Band '{band[1]}' (ID: {band[0]}) has been updated.")
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def delete_band():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID to delete: ")

    # Find the band by name or ID
    if band_name_or_id.isdigit():
        band = Band.find_by_id(band_name_or_id)
    else:
        band = Band.find_by_name(band_name_or_id)

    if not band:
        print(Fore.RED + "Error: Band not found.")
        return

    Band.delete(band[0])
    print(Fore.GREEN + f"Band '{band[1]}' (ID: {band[0]}) has been deleted.")

def view_band_related_tours():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID: ")

    if band_name_or_id.isdigit():
        band = Band.find_by_id(band_name_or_id)
    else:
        band = Band.find_by_name(band_name_or_id)

    if not band:
        print(Fore.RED + "Error: Band not found.")
        return

    tour_dates = TourDate.find_by_band(band[0])
    if not tour_dates:
        print(Fore.RED + "No tours found for this band.")
    else:
        for tour in tour_dates:
            print(Fore.YELLOW + f"ID: {tour[0]}, Location: {tour[2]}, Date: {tour[3]}, Venue: {tour[4]}")

def view_tour_dates():
    print(Fore.BLUE + "How would you like to filter the tour dates?")
    print(Fore.CYAN + "1. By Band")
    print(Fore.CYAN + "2. By Location")
    print(Fore.CYAN + "3. By Venue")
    print(Fore.CYAN + "4. View All Tour Dates")
    
    choice = input(Fore.YELLOW + "> ")

    if choice == "1":
        band_name_or_id = input(Fore.CYAN + "Enter the band name or ID: ")
        if band_name_or_id.isdigit():
            band = Band.find_by_id(band_name_or_id)
        else:
            band = Band.find_by_name(band_name_or_id)

        if not band:
            print(Fore.RED + "Band not found.")
            return
        
        # Fetch tour dates for the band
        tour_dates = TourDate.find_by_band(band[0])
        if not tour_dates:
            print(Fore.RED + f"No tour dates found for band {band[1]}.")
        else:
            for tour in tour_dates:
                location_color = ColorManager.get_location_color(tour[3])
                print(location_color + f"ID: {tour[0]}, Band: {tour[2]} (ID: {tour[1]}), Location: {tour[3]}, Date: {tour[4]}, Venue: {tour[5]}")

    elif choice == "2":
        location = input(Fore.CYAN + "Enter the location: ")
        tour_dates = TourDate.find_by_location(location)

        if not tour_dates:
            print(Fore.RED + f"No tour dates found at location '{location}'.")
        else:
            for tour in tour_dates:
                location_color = ColorManager.get_location_color(tour[3])
                print(location_color + f"ID: {tour[0]}, Band: {tour[2]} (ID: {tour[1]}), Location: {tour[3]}, Date: {tour[4]}, Venue: {tour[5]}")

    elif choice == "3":
        venue = input(Fore.CYAN + "Enter the venue: ")
        tour_dates = TourDate.find_by_venue(venue)

        if not tour_dates:
            print(Fore.RED + f"No tour dates found at venue '{venue}'.")
        else:
            for tour in tour_dates:
                location_color = ColorManager.get_location_color(tour[3])
                print(location_color + f"ID: {tour[0]}, Band: {tour[2]} (ID: {tour[1]}), Location: {tour[3]}, Date: {tour[4]}, Venue: {tour[5]}")

    elif choice == "4":
        # View all tour dates in chronological order
        tour_dates = TourDate.all_chronological()

        if not tour_dates:
            print(Fore.RED + "No tour dates found.")
        else:
            for tour in tour_dates:
                location_color = ColorManager.get_location_color(tour[3])
                print(location_color + f"ID: {tour[0]}, Band: {tour[2]} (ID: {tour[1]}), Location: {tour[3]}, Date: {tour[4]}, Venue: {tour[5]}")
    else:
        print(Fore.RED + "Invalid choice. Please select a valid option.")

def schedule_tour_date():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID: ")

    if band_name_or_id.isdigit():
        band = Band.find_by_id(band_name_or_id)
    else:
        band = Band.find_by_name(band_name_or_id)

    if not band:
        print(Fore.RED + "Error: Band not found.")
        return

    location = input(Fore.CYAN + "Enter location: ")  

    # Get date from calendar
    date = select_date_gui()
    formatted_date = format_date(date)

    # Validate that the date is in the future
    if not validate_future_date(formatted_date):
        print(Fore.RED + "Error: The selected date is in the past. Please select a future date.")
        return

    venue = input(Fore.CYAN + "Enter venue: ")

    # Check if the venue is already booked for the selected date
    existing_tour = TourDate.find_by_venue_and_date(venue, formatted_date)
    if existing_tour:
        print(Fore.RED + f"Error: The venue '{venue}' is already booked on {formatted_date}.")
        return

    # If everything is valid, proceed with creating the tour date
    TourDate.create(band[0], location, formatted_date, venue)
    print(Fore.GREEN + "Tour date created.")

def update_tour_date():
    use_tour_id = input(Fore.CYAN + "Do you know the tour ID? (y/n): ").lower()
    
    if use_tour_id == 'y':
        tour_id = input(Fore.CYAN + "Enter the Tour ID: ")
        tour = TourDate.find_by_id(tour_id)
        if not tour:
            print(Fore.RED + "Tour not found.")
            return
    else:
        venue = input(Fore.CYAN + "Enter the venue: ")
        print(Fore.CYAN + "Select the tour date:")
        date = select_date_gui()
        formatted_date = format_date(date)
        tour = TourDate.find_by_venue_and_date(venue, formatted_date)
        if not tour:
            print(Fore.RED + "Tour not found.")
            return
    
    band = Band.find_by_id(tour[1])
    if band:
        print(Fore.GREEN + f"Tour at '{tour[4]}' on {tour[3]} for Band '{band[1]}' has been found.")
    else:
        print(Fore.GREEN + f"Tour at '{tour[4]}' on {tour[3]} for Band ID {tour[1]} has been found.")
    
    new_location = input(Fore.CYAN + f"Enter new location for tour (current: {tour[2]}) (leave blank to keep current): ")

    print(Fore.CYAN + "Select the new tour date:")
    new_date = select_date_gui()
    formatted_new_date = format_date(new_date)

    if not validate_future_date(formatted_new_date):
        print(Fore.RED + "Error: You cannot select a date in the past.")
        return

    new_venue = input(Fore.CYAN + f"Enter new venue for tour (current: {tour[4]}) (leave blank to keep current): ")

    TourDate.update(
        tour[0], 
        new_location if new_location else None, 
        formatted_new_date if new_date else None, 
        new_venue if new_venue else None
    )
    print(Fore.GREEN + f"Tour at '{new_location}' on {formatted_new_date} for Band '{band[1]}' has been updated.")

def delete_tour_date():
    use_tour_id = input(Fore.CYAN + "Do you know the tour ID? (y/n): ").lower()
    
    if use_tour_id == 'y':
        tour_id = input(Fore.CYAN + "Enter the Tour ID: ")
        tour = TourDate.find_by_id(tour_id)
        if not tour:
            print(Fore.RED + "Tour not found.")
            return
    else:
        venue = input(Fore.CYAN + "Enter the venue: ")
        print(Fore.CYAN + "Select the tour date:")
        date = select_date_gui()
        formatted_date = format_date(date)
        tour = TourDate.find_by_venue_and_date(venue, formatted_date)
        if not tour:
            print(Fore.RED + "Tour not found.")
            return

    band = Band.find_by_id(tour[1])
    if band:
        print(Fore.GREEN + f"Tour at '{tour[4]}' on {tour[3]} for Band '{band[1]}' has been deleted.")
    else:
        print(Fore.GREEN + f"Tour at '{tour[4]}' on {tour[3]} for Band ID {tour[1]} has been deleted.")

    TourDate.delete(tour[0])

def view_tour_related_band():
    tour_id = input(Fore.CYAN + "Enter the tour ID: ")

    tour = TourDate.find_by_id(tour_id)

    if not tour:
        print(Fore.RED + "Error: Tour not found.")
        return

    band = Band.find_by_id(tour[1])
    if band:
        print(Fore.YELLOW + f"Band Name: {band[1]}, Genre: {band[2]}")
    else:
        print(Fore.RED + "Band not found for this tour.")

# Entry point for the CLI application
if __name__ == "__main__":
    main()
