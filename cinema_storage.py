import json

from booking import Booking
from cinema import Cinema
from hall import Hall
from movie import Movie
from screening import Screening


def load_movies(filename: str = "movies.json") -> list[Movie]:
    with open(filename, encoding="utf-8") as file:
        rows = json.load(file)
    return [Movie(row["movie_id"], row["title"], row["release_year"],
                  row["duration_minutes"]) for row in rows]


def load_halls(filename: str = "halls.json") -> list[Hall]:
    with open(filename, encoding="utf-8") as file:
        rows = json.load(file)
    return [Hall(row["hall_id"], row["name"], row["seat_count"]) for row in rows]


def load_screenings(filename: str = "screenings.json") -> list[Screening]:
    with open(filename, encoding="utf-8") as file:
        rows = json.load(file)
    return [Screening(row["screening_id"], row["movie_id"], row["hall_id"],
                      row["starts_at"], row["price"]) for row in rows]


def load_bookings(filename: str = "bookings.json") -> list[Booking]:
    with open(filename, encoding="utf-8") as file:
        rows = json.load(file)
    return [Booking(row["booking_id"], row["screening_id"], row["customer_name"],
                    row["seat_number"], row["status"]) for row in rows]


def load_cinema() -> Cinema:
    return Cinema(load_movies(), load_halls(), load_screenings(), load_bookings())


def save_bookings(bookings: list[Booking], filename: str = "bookings.json") -> None:
    rows = []
    for booking in bookings:
        rows.append({
            "booking_id": booking.booking_id,
            "screening_id": booking.screening_id,
            "customer_name": booking.customer_name,
            "seat_number": booking.seat_number,
            "status": "active",
        })
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
        file.write("\n")
