from booking import Booking
from hall import Hall
from movie import Movie
from screening import Screening


class Cinema:
    def __init__(self, movies: list[Movie], halls: list[Hall],
                 screenings: list[Screening], bookings: list[Booking]):
        self.movies = movies
        self.halls = halls
        self.screenings = screenings
        self.bookings = bookings

    def get_movie(self, movie_id: str) -> Movie:
        for movie in self.movies:
            if movie.movie_id == movie_id:
                return movie
        raise ValueError("映画が見つかりません")

    def get_hall(self, hall_id: str) -> Hall:
        for hall in self.halls:
            if hall.hall_id == hall_id:
                return hall
        raise ValueError("ホールが見つかりません")

    def get_screening(self, screening_id: str) -> Screening:
        for screening in self.screenings:
            if screening.screening_id == screening_id:
                return screening
        raise ValueError("上映回が見つかりません")

    def get_booking(self, booking_id: str) -> Booking:
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        raise ValueError("予約が見つかりません")

    def get_booked_seats(self, screening_id: str) -> list[int]:
        screening = self.get_screening(screening_id)
        seats = []
        for booking in self.bookings:
            booked_screening = self.get_screening(booking.screening_id)
            if booked_screening.hall_id == screening.hall_id:
                seats.append(booking.seat_number)
        return seats

    def get_available_seats(self, screening_id: str) -> list[int]:
        screening = self.get_screening(screening_id)
        hall = self.get_hall(screening.hall_id)
        booked_seats = self.get_booked_seats(screening_id)
        return [seat for seat in range(1, hall.seat_count + 1)
                if seat not in booked_seats]

    def create_booking(self, screening_id: str, customer_name: str,
                       seat_number: int) -> Booking:
        self.get_screening(screening_id)
        customer_name = customer_name.strip()
        if not customer_name:
            raise ValueError("予約者名を入力してください")
        hall = self.halls[0]
        if not hall.is_valid_seat(seat_number):
            raise ValueError("座席番号が範囲外です")
        if seat_number in self.get_booked_seats(screening_id):
            raise ValueError("この座席は予約済みです")
        next_number = max(
            (int(booking.booking_id[1:]) for booking in self.bookings),
            default=0,
        ) + 1
        booking = Booking(f"B{next_number:03d}", screening_id,
                          customer_name, seat_number)
        self.bookings.append(booking)
        return booking

    def cancel_booking(self, booking_id: str) -> None:
        self.get_booking(booking_id).cancel()
