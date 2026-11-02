import json

import pytest

from booking import Booking
from cinema import Cinema
from cinema_storage import load_bookings, load_cinema, save_bookings
from hall import Hall
from movie import Movie
from screening import Screening


@pytest.fixture
def cinema():
    movies = [Movie("M001", "テスト映画", 2026, 100)]
    halls = [Hall("H01", "第1ホール", 80), Hall("H02", "第2ホール", 20)]
    screenings = [
        Screening("S001", "M001", "H01", "2026-11-14 10:00", 1500),
        Screening("S002", "M001", "H01", "2026-11-14 15:00", 1500),
        Screening("S003", "M001", "H02", "2026-11-14 10:00", 2200),
    ]
    return Cinema(movies, halls, screenings, [])


def test_get_movie_returns_original_object(cinema):
    movie = cinema.get_movie("M001")
    assert movie is cinema.movies[0]
    assert movie.title == "テスト映画"


def test_unknown_screening_raises_error(cinema):
    with pytest.raises(ValueError, match="上映回が見つかりません"):
        cinema.get_screening("S999")
    assert cinema.bookings == []


def test_empty_screening_has_all_seats(cinema):
    seats = cinema.get_available_seats("S001")
    assert seats == list(range(1, 81))
    assert cinema.bookings == []


def test_create_booking_stores_customer_and_seat(cinema):
    booking = cinema.create_booking("S001", "  田中 美咲  ", 10)
    assert booking.booking_id == "B001"
    assert booking.screening_id == "S001"
    assert booking.customer_name == "田中 美咲"
    assert booking.seat_number == 10
    assert booking.status == "active"
    assert cinema.get_booking(booking.booking_id) is booking
    assert 10 not in cinema.get_available_seats("S001")


def test_same_screening_cannot_book_same_seat_twice(cinema):
    first = cinema.create_booking("S001", "田中", 10)
    with pytest.raises(ValueError, match="この座席は予約済みです"):
        cinema.create_booking("S001", "佐藤", 10)
    assert cinema.bookings == [first]
    assert first.status == "active"


@pytest.mark.parametrize("seat_number", [0, -1, 81])
def test_invalid_seat_in_first_hall_does_not_create_booking(cinema, seat_number):
    with pytest.raises(ValueError, match="座席番号が範囲外です"):
        cinema.create_booking("S001", "田中", seat_number)
    assert cinema.bookings == []


def test_blank_customer_name_does_not_create_booking(cinema):
    with pytest.raises(ValueError, match="予約者名を入力してください"):
        cinema.create_booking("S001", "   ", 10)
    assert cinema.bookings == []


def test_cancel_changes_booking_status(cinema):
    booking = cinema.create_booking("S001", "田中", 10)
    cinema.cancel_booking(booking.booking_id)
    assert booking.status == "cancelled"
    assert cinema.get_booking(booking.booking_id) is booking


def test_repeated_cancellation_raises_error(cinema):
    booking = cinema.create_booking("S001", "田中", 10)
    cinema.cancel_booking(booking.booking_id)
    with pytest.raises(ValueError, match="この予約はキャンセル済みです"):
        cinema.cancel_booking(booking.booking_id)
    assert booking.status == "cancelled"


def test_active_booking_can_be_saved_and_loaded(tmp_path):
    filename = str(tmp_path / "bookings.json")
    original = Booking("B012", "S001", "田中 美咲", 10)
    save_bookings([original], filename)
    loaded = load_bookings(filename)
    assert len(loaded) == 1
    assert loaded[0] is not original
    assert vars(loaded[0]) == vars(original)
    with open(filename, encoding="utf-8") as file:
        rows = json.load(file)
    assert rows[0]["seat_number"] == 10


def test_empty_bookings_can_be_saved_and_loaded(tmp_path):
    filename = str(tmp_path / "bookings.json")
    save_bookings([], filename)
    assert load_bookings(filename) == []


def test_new_booking_id_uses_largest_existing_number(cinema):
    cinema.bookings = [Booking("B009", "S001", "佐藤", 1),
                       Booking("B003", "S001", "鈴木", 2)]
    new_booking = cinema.create_booking("S001", "田中", 10)
    assert new_booking.booking_id == "B010"
    assert len({booking.booking_id for booking in cinema.bookings}) == 3


def test_distributed_data_can_be_loaded():
    cinema = load_cinema()
    assert len(cinema.movies) == 8
    assert len(cinema.halls) == 5
    assert len(cinema.screenings) == 30
    assert len({booking.booking_id for booking in cinema.bookings}) == len(cinema.bookings)
    for screening in cinema.screenings:
        assert cinema.get_movie(screening.movie_id).duration_minutes > 0
        assert cinema.get_hall(screening.hall_id).seat_count > 0
