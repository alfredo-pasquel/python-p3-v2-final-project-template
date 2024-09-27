from models.__init__ import CONN, CURSOR

class Band:
    def __init__(self, name, genre):
        self._name = None
        self._genre = None
        self.name = name  # This will call the setter
        self.genre = genre  # This will call the setter

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (0 < len(value) <= 50):
            raise ValueError("Band name must be between 1 and 50 characters.")
        self._name = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        if not (0 < len(value) <= 30):
            raise ValueError("Genre must be between 1 and 30 characters.")
        self._genre = value

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
        if new_name:
            CURSOR.execute("UPDATE bands SET name = ? WHERE id = ?", (new_name, band_id))
        if new_genre:
            CURSOR.execute("UPDATE bands SET genre = ? WHERE id = ?", (new_genre, band_id))
        CONN.commit()

    @classmethod
    def delete(cls, band_id):
        CURSOR.execute("DELETE FROM bands WHERE id = ?", (band_id,))
        CONN.commit()
    
    @classmethod
    def find_by_id(cls, band_id):
        return CURSOR.execute("SELECT * FROM bands WHERE id = ?", (band_id,)).fetchone()
    
    @classmethod
    def find_by_name(cls, name):
        return CURSOR.execute("SELECT * FROM bands WHERE name = ?", (name,)).fetchone()