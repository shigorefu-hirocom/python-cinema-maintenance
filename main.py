from cinema import Cinema
from cinema_storage import load_cinema, save_bookings


def show_movies(cinema: Cinema) -> None:
    for movie in cinema.movies:
        print(f"{movie.movie_id}: {movie.title} "
              f"({movie.release_year}年 / {movie.duration_minutes}分)")


def show_screenings(cinema: Cinema) -> None:
    for screening in cinema.screenings:
        movie = cinema.get_movie(screening.movie_id)
        hall = cinema.get_hall(screening.hall_id)
        print(f"{screening.screening_id}: {screening.starts_at} / "
              f"{movie.title} / {hall.name} / {screening.price}円")


def show_available_seats(cinema: Cinema) -> None:
    screening_id = input("上映回ID: ").strip()
    seats = cinema.get_available_seats(screening_id)
    print(f"空席数: {len(seats)}")
    print("空席: " + (", ".join(str(seat) for seat in seats) if seats else "満席"))


def book_seat(cinema: Cinema) -> None:
    screening_id = input("上映回ID: ").strip()
    customer_name = input("予約者名: ")
    seat_text = input("座席番号: ").strip()
    try:
        seat_number = int(seat_text)
    except ValueError:
        raise ValueError("座席番号は整数で入力してください") from None
    booking = cinema.create_booking(screening_id, customer_name, seat_number)
    save_bookings(cinema.bookings)
    screening = cinema.get_screening(screening_id)
    print(f"予約完了: {booking.booking_id} / {booking.customer_name} / "
          f"座席{booking.seat_number} / {screening.price}円")


def cancel_booking(cinema: Cinema) -> None:
    booking_id = input("予約ID: ").strip()
    cinema.cancel_booking(booking_id)
    save_bookings(cinema.bookings)
    print(f"キャンセル完了: {booking_id}")


def show_bookings(cinema: Cinema) -> None:
    for booking in cinema.bookings:
        screening = cinema.get_screening(booking.screening_id)
        movie = cinema.get_movie(screening.movie_id)
        status = "予約中" if booking.status == "active" else "キャンセル済み"
        print(f"{booking.booking_id}: {booking.screening_id} / "
              f"{screening.starts_at} / {movie.title} / "
              f"{booking.customer_name} / 座席{booking.seat_number} [{status}]")
    if not cinema.bookings:
        print("予約はありません")


def main() -> None:
    cinema = load_cinema()
    actions = {
        "1": show_movies,
        "2": show_screenings,
        "3": show_available_seats,
        "4": book_seat,
        "5": cancel_booking,
        "6": show_bookings,
    }
    while True:
        print("\nひろこむシネマ 予約管理システム")
        print("1. 映画一覧\n2. 上映スケジュール\n3. 空席確認")
        print("4. 新規予約\n5. 予約キャンセル\n6. 予約一覧\n0. 終了")
        try:
            choice = input("操作を選択: ").strip()
            if choice == "0":
                print("終了しました")
                break
            action = actions.get(choice)
            if action is None:
                print("メニューの番号を入力してください")
                continue
            try:
                action(cinema)
            except ValueError as error:
                print(f"操作できません: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\n終了しました")
            break


if __name__ == "__main__":
    main()
