from models.__init__ import CONN, CURSOR

class TourDate:
    def __init__(self, location, date, venue):
        self._location = None
        self._date = None
        self._venue = None
        self.location = location  # This will call the setter
        self.date = date  # This will call the setter
        self.venue = venue  # This will call the setter

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not value:
            raise ValueError("Location cannot be empty.")
        self._location = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def venue(self):
        return self._venue

    @venue.setter
    def venue(self, value):
        if not value:
            raise ValueError("Venue cannot be empty.")
        self._venue = value

    @classmethod
    def all(cls):
        return CURSOR.execute("SELECT * FROM tour_dates").fetchall()

    @classmethod
    def create(cls, band_id, location, date, venue):
        tour_date = cls(location, date, venue)
        CURSOR.execute("INSERT INTO tour_dates (band_id, location, date, venue) VALUES (?, ?, ?, ?)", 
                       (band_id, tour_date.location, tour_date.date, tour_date.venue))
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
            WHERE tour_dates.location = ?
            ORDER BY tour_dates.date
        """, (location,)).fetchall()

    @classmethod
    def find_by_venue(cls, venue):
        return CURSOR.execute("""
            SELECT tour_dates.id, bands.id, bands.name, tour_dates.location, tour_dates.date, tour_dates.venue 
            FROM tour_dates
            JOIN bands ON tour_dates.band_id = bands.id
            WHERE tour_dates.venue = ?
            ORDER BY tour_dates.date
        """, (venue,)).fetchall()

    @classmethod
    def find_by_venue_and_date(cls, venue, date):
        return CURSOR.execute("SELECT * FROM tour_dates WHERE venue = ? AND date = ?", (venue, date)).fetchone()

    @classmethod
    def all_chronological(cls):
        return CURSOR.execute("""
            SELECT tour_dates.id, bands.id, bands.name, tour_dates.location, tour_dates.date, tour_dates.venue 
            FROM tour_dates
            JOIN bands ON tour_dates.band_id = bands.id
            ORDER BY tour_dates.date
        """).fetchall()
