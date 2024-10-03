#!/usr/bin/env python3

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
    
    used_genre_colors = set()
    used_location_colors = set()

    @classmethod
    def get_genre_color(cls, genre):
        if genre not in cls.genre_colors:
            available_colors = [color for color in cls.COLORS if color not in cls.used_genre_colors]
            
            if not available_colors:
                cls.used_genre_colors.clear()
                available_colors = cls.COLORS.copy()

            selected_color = random.choice(available_colors)
            cls.genre_colors[genre] = selected_color
            cls.used_genre_colors.add(selected_color)

        return cls.genre_colors[genre]

    @classmethod
    def get_location_color(cls, location):
        normalized_location = location.strip().lower()

        if normalized_location not in cls.location_colors:
            available_colors = [color for color in cls.COLORS if color not in cls.used_location_colors]
            
            if not available_colors:
                cls.used_location_colors.clear()
                available_colors = cls.COLORS.copy()

            selected_color = random.choice(available_colors)
            cls.location_colors[normalized_location] = selected_color
            cls.used_location_colors.add(selected_color)

        return cls.location_colors[normalized_location]

def select_date_gui():
    selected_date = None
    
    root = tk.Tk()
    root.title("Select a Date")

    cal = Calendar(root, selectmode='day', year=2024, month=10, day=1)
    cal.pack(pady=20)

    def grab_date():
        nonlocal selected_date
        selected_date = cal.get_date()
        root.quit()

    select_btn = tk.Button(root, text="Select", command=grab_date)
    select_btn.pack(pady=20)

    root.mainloop()
    root.destroy()
    
    return selected_date

def format_date(date_str):
    try:

        formatted_date = datetime.strptime(date_str, "%m/%d/%y").strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        try:

            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            return formatted_date
        except ValueError as e:
            
            print(f"Error formatting date: {date_str}")
            print(f"Exception: {e}")
            raise e

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

        if band_name_or_id.isdigit():
            band = Band.find_by_id(band_name_or_id)
        else:
            band = Band.find_by_name(band_name_or_id)

        if not band:
            print(Fore.RED + "Band not found.")
        else:

            genre_color = ColorManager.get_genre_color(band[2])  
            print(genre_color + f"ID: {band[0]}, Name: {band[1]}, Genre: {band[2]}")
    else:

        bands = Band.all()
        for band in bands:

            genre_color = ColorManager.get_genre_color(band[2])
            print(genre_color + f"ID: {band[0]}, Name: {band[1]}, Genre: {band[2]}")

def create_band():

    try:
        name = input(Fore.CYAN + "Enter band name: ")
        genre = input(Fore.CYAN + "Enter genre: ")
        Band.create(name, genre)
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def update_band():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID to update: ").strip().lower()

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
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def delete_band():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID to delete: ")

    if band_name_or_id.isdigit():
        band = Band.find_by_id(band_name_or_id)
    else:
        band = Band.find_by_name(band_name_or_id)

    if not band:
        print(Fore.RED + "Error: Band not found.")
        return

    Band.delete(band[0])

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
            print(Fore.YELLOW + f"ID: {tour[0]}, Location: {tour[3]}, Date: {tour[4]}, Venue: {tour[5]}")

def view_tour_dates():
    print(Fore.BLUE + "How would you like to filter the tour dates?")
    print(Fore.CYAN + "1. By Band")
    print(Fore.CYAN + "2. By Location")
    print(Fore.CYAN + "3. By Venue")
    print(Fore.CYAN + "4. View All Tour Dates")
    
    choice = input(Fore.YELLOW + "> ").strip().lower()

    if choice == "1":
        band_name_or_id = input(Fore.CYAN + "Enter the band name or ID: ").strip().lower()
        if band_name_or_id.isdigit():
            band = Band.find_by_id(band_name_or_id)
        else:
            band = Band.find_by_name(band_name_or_id)

        if not band:
            print(Fore.RED + "Band not found.")
            return
        
        tour_dates = TourDate.find_by_band(band[0])
        display_tour_dates(tour_dates, f"No tour dates found for band {band[1]}.")

    elif choice == "2":
        location = input(Fore.CYAN + "Enter the location: ").strip().lower()
        tour_dates = TourDate.find_by_location(location)
        display_tour_dates(tour_dates, f"No tour dates found at location '{location}'.")

    elif choice == "3":
        venue = input(Fore.CYAN + "Enter the venue: ").strip().lower()
        tour_dates = TourDate.find_by_venue(venue)
        display_tour_dates(tour_dates, f"No tour dates found at venue '{venue}'.")

    elif choice == "4":
        tour_dates = TourDate.all_chronological()
        display_tour_dates(tour_dates, "No tour dates found.")

    else:
        print(Fore.RED + "Invalid choice. Please select a valid option.")

def display_tour_dates(tour_dates, not_found_message):
    
    if not tour_dates:
        print(Fore.RED + not_found_message)
    else:
        for tour in tour_dates:
            location_color = ColorManager.get_location_color(tour[3])
            print(location_color + f"ID: {tour[0]}, Band: {tour[2]} (Band ID: {tour[1]}), Location: {tour[3]}, Date: {tour[4]}, Venue: {tour[5]}")

def schedule_tour_date():
    band_name_or_id = input(Fore.CYAN + "Enter the band name or ID: ").strip().lower()

    if band_name_or_id.isdigit():
        band = Band.find_by_id(band_name_or_id)
    else:
        band = Band.find_by_name(band_name_or_id)

    if not band:
        print(Fore.RED + "Error: Band not found.")
        return

    location = input(Fore.CYAN + "Enter location: ").strip().lower()  

    date = select_date_gui()
    formatted_date = format_date(date)

    venue = input(Fore.CYAN + "Enter venue: ").strip().lower()

    try:
        TourDate.create(band[0], location, formatted_date, venue)
        print(Fore.GREEN + "Tour date created.")
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def update_tour_date():
    use_tour_id = input(Fore.CYAN + "Do you know the tour ID? (y/n): ").strip().lower()

    if use_tour_id == 'y':
        tour_id = input(Fore.CYAN + "Enter the Tour ID: ")
        tour = TourDate.find_by_id(tour_id)
        if not tour:
            print(Fore.RED + "Tour not found.")
            return
    else:
        venue = input(Fore.CYAN + "Enter the venue: ").strip().lower()
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

    new_location = input(Fore.CYAN + f"Enter new location for tour (current: {tour[2]}) (leave blank to keep current): ").strip().lower()

    print(Fore.CYAN + "Select the new tour date:")
    new_date = select_date_gui()
    formatted_new_date = format_date(new_date)

    new_venue = input(Fore.CYAN + f"Enter new venue for tour (current: {tour[4]}) (leave blank to keep current): ").strip().lower()

    try:

        TourDate.update(
            tour[0], 
            new_location if new_location else None, 
            formatted_new_date if new_date else None, 
            new_venue if new_venue else None
        )
        print(Fore.GREEN + f"Tour at '{new_location if new_location else tour[2]}' on {formatted_new_date} for Band '{band[1]}' has been updated.")
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def delete_tour_date():
    use_tour_id = input(Fore.CYAN + "Do you know the tour ID? (y/n): ").strip().lower()
    
    if use_tour_id == 'y':
        tour_id = input(Fore.CYAN + "Enter the Tour ID: ").strip()
        tour = TourDate.find_by_id(tour_id)
        if not tour:
            print(Fore.RED + "Tour not found.")
            return
    else:
        venue = input(Fore.CYAN + "Enter the venue: ").strip().lower()
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
        print(Fore.GREEN + f"Tour at '{tour[4]}' on {tour[3]} for Band '{band[1]}' has been deleted.")

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

if __name__ == "__main__":
    main()
