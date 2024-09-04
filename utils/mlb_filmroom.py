import datetime

FILM_ROOM_ROOT_URL = "https://www.mlb.com/video/?q=Season+%3D+%5B{year}%5D+AND+Date+%3D+%5B%22{date}%22%5D+AND+PitcherId+%3D+%5B{pitcher_id}%5D+AND+TopBottom+%3D+%5B%22{inning_top_bot}%22%5D+AND+Outs+%3D+%5B{outs}%5D+AND+Balls+%3D+%5B{balls}%5D+AND+Strikes+%3D+%5B{strikes}%5D+AND+Inning+%3D+%5B{inning}%5D+AND+PlayerId+%3D+%5B{hitter_id}%5D+AND+PitchType+%3D+%5B%22{pitch_type}%22%5D+Order+By+Timestamp+DESC"

FILM_ROOM_SEARCH_COLUMNS = [
    "pitcher",
    "batter",
    "pitch_type",
    "inning",
    "inning_top_bot",
    "outs_when_up",
    "balls",
    "strikes",
]


def search_mlb_film_room(pitch_row_dict: dict, date: datetime.datetime) -> str:
    """hacks the mlb film room search url to find the video of a specific pitch"""
    year = date.year

    cur_pitch_url = FILM_ROOM_ROOT_URL.format(
        **pitch_row_dict, year=year, date=date.strftime("%Y-%m-%d")
    )
    return cur_pitch_url


if __name__ == "__main__":
    link = search_mlb_film_room(
        pitch_row_dict={
            "pitcher_id": 687924,
            "hitter_id": 680474,
            "pitch_type": "SL",
            "inning": 2,
            "inning_top_bot": "TOP",
            "outs": 0,
            "balls": 0,
            "strikes": 0,
        },
        date=datetime.datetime(2024, 8, 29),
    )

    print(link)
