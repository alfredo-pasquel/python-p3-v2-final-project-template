from models.__init__ import CONN, CURSOR

class Band:
    def __init__(self, name, genre):
        self.name = name  # Calls the setter
        self.genre = genre  # Calls the setter

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Ensure band name is unique
        if Band.find_by_name(value):
            raise ValueError(f"Band name '{value}' is already taken.")
        if not (0 < len(value) <= 50):
            raise ValueError("Band name must be between 1 and 50 characters.")
        if not value.strip():
            raise ValueError("Band name cannot be empty.")
        self._name = value.strip().lower()

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        if not (0 < len(value) <= 30):
            raise ValueError("Genre must be between 1 and 30 characters.")
        if not value.strip():
            raise ValueError("Genre cannot be empty.")
        self._genre = value.strip().lower()

    @classmethod
    def all(cls):
        return CURSOR.execute("SELECT * FROM bands").fetchall()

    @classmethod
    def create(cls, name, genre):
        band = cls(name, genre)
        CURSOR.execute("INSERT INTO bands (name, genre) VALUES (?, ?)", (band.name, band.genre))
        CONN.commit()
        print(f"Band '{band.name}' created successfully.")

    @classmethod
    def update(cls, band_id, new_name=None, new_genre=None):
        band = cls.find_by_id(band_id)  # Fetch the current band data
        
        # Use current values if no new ones are provided
        name_to_update = new_name.strip().lower() if new_name else band[1].strip().lower()  # Current name is at index 1
        genre_to_update = new_genre.strip().lower() if new_genre else band[2].strip().lower()  # Normalize genre to lowercase

        # Only check uniqueness if a new name is provided AND it's different from the current one
        if new_name and new_name.strip() and new_name.strip().lower() != band[1].strip().lower():
            if Band.find_by_name(new_name.strip().lower()):
                raise ValueError(f"Band name '{new_name}' is already taken.")

        # Perform the database update using current or new values
        CURSOR.execute("UPDATE bands SET name = ?, genre = ? WHERE id = ?", 
                    (name_to_update, genre_to_update, band_id))
        CONN.commit()
        print(f"Band '{name_to_update}' with genre '{genre_to_update}' updated successfully.")

    @classmethod
    def delete(cls, band_id):
        # Fetch the band details before deletion
        band = cls.find_by_id(band_id)
        
        if not band:
            print(f"Band with ID {band_id} not found.")
            return

        # Proceed to delete the band
        CURSOR.execute("DELETE FROM bands WHERE id = ?", (band_id,))
        CONN.commit()

        # Print the deleted band's details
        print(f"Band '{band[1]}' with genre '{band[2]}' has been successfully deleted.")

        
    @classmethod
    def find_by_id(cls, band_id):
        return CURSOR.execute("SELECT * FROM bands WHERE id = ?", (band_id,)).fetchone()

    @classmethod
    def find_by_name(cls, name):
        return CURSOR.execute("SELECT * FROM bands WHERE name = ?", (name.strip().lower(),)).fetchone()
