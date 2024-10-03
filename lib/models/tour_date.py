from models.__init__ import CONN, CURSOR
from datetime import datetime

class TourDate:
    def __init__(self, band_id, location, date, venue):
        self.band_id = band_id
        self.location = location
        self.date = date
        self.venue = venue

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not value.strip():
            raise ValueError("Location cannot be empty.")
        self._location = value.strip().lower()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):

        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d")

        if value < datetime.now():
            raise ValueError("Tour date cannot be in the past.")
        self._date = value

    @property
    def venue(self):
        return self._venue

    @venue.setter
    def venue(self, value):
        
        result = TourDate.find_by_venue_and_date(value, self.date)
        
        if result:
            raise ValueError("This venue is already booked for that date.")
        
        if not value.strip():
            raise ValueError("Venue cannot be empty.")
        
        self._venue = value.strip().lower()

    @classmethod
    def all(cls):
        return CURSOR.execute("SELECT * FROM tour_dates").fetchall()

    @classmethod
    def create(cls, band_id, location, date, venue):
        tour_date = cls(band_id, location, date, venue)
        CURSOR.execute("INSERT INTO tour_dates (band_id, location, date, venue) VALUES (?, ?, ?, ?)", 
                       (tour_date.band_id, tour_date.location, tour_date.date, tour_date.venue))
        CONN.commit()
        print(f"Tour date created for band with ID {band_id}.")

    @classmethod
    def update(cls, tour_id, new_location=None, new_date=None, new_venue=None):
        if new_location:
            CURSOR.execute("UPDATE tour_dates SET location = ? WHERE id = ?", (new_location, tour_id))
        if new_date:
            CURSOR.execute("UPDATE tour_dates SET date = ? WHERE id = ?", (new_date, tour_id))
        if new_venue:
            CURSOR.execute("UPDATE tour_dates SET venue = ? WHERE id = ?", (new_venue, tour_id))
        CONN.commit()
        print(f"Tour date with ID {tour_id} has been updated.")

    @classmethod
    def delete(cls, tour_id):
        CURSOR.execute("DELETE FROM tour_dates WHERE id = ?", (tour_id,))
        CONN.commit()

    @classmethod
    def find_by_id(cls, tour_id):
        return CURSOR.execute("SELECT * FROM tour_dates WHERE id = ?", (tour_id,)).fetchone()

    @classmethod
    def find_by_band(cls, band_id):
        return CURSOR.execute("""
            SELECT tour_dates.id, bands.id, bands.name, tour_dates.location, tour_dates.date, tour_dates.venue 
            FROM tour_dates
            JOIN bands ON tour_dates.band_id = bands.id
            WHERE tour_dates.band_id = ?
            ORDER BY tour_dates.date
        """, (band_id,)).fetchall()
    
    @classmethod
    def find_by_location(cls, location):
        return CURSOR.execute("""
            SELECT tour_dates.id, bands.id, bands.name, tour_dates.location, tour_dates.date, tour_dates.venue 
            FROM tour_dates
            JOIN bands ON tour_dates.band_id = bands.id
            WHERE LOWER(tour_dates.location) = ?
            ORDER BY tour_dates.date
        """, (location.strip().lower(),)).fetchall()

    @classmethod
    def find_by_venue(cls, venue):
        return CURSOR.execute("""
            SELECT tour_dates.id, bands.id, bands.name, tour_dates.location, tour_dates.date, tour_dates.venue 
            FROM tour_dates
            JOIN bands ON tour_dates.band_id = bands.id
            WHERE LOWER(tour_dates.venue) = ?
            ORDER BY tour_dates.date
        """, (venue.strip().lower(),)).fetchall()

    @classmethod
    def find_by_venue_and_date(cls, venue, date):
        return CURSOR.execute(
            "SELECT * FROM tour_dates WHERE LOWER(venue) = ? AND DATE(date) = DATE(?)",
            (venue.strip().lower(), date)
        ).fetchone()

    @classmethod
    def all_chronological(cls):
        return CURSOR.execute("""
            SELECT tour_dates.id, bands.id, bands.name, tour_dates.location, tour_dates.date, tour_dates.venue 
            FROM tour_dates
            JOIN bands ON tour_dates.band_id = bands.id
            ORDER BY tour_dates.date
        """).fetchall()
