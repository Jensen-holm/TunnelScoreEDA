from typing import Optional
import datetime
from pprint import pprint

FILM_ROOM_ROOT_URL = "https://www.mlb.com/video/?q=Season+%3D+%5B{year}%5D+AND+Date+%3D+%5B%22{date}%22%5D+AND+PitcherId+%3D+%5B{pitcher}%5D+AND+TopBottom+%3D+%5B%22{inning_top_bot}%22%5D+AND+Outs+%3D+%5B{outs}%5D+AND+Balls+%3D+%5B{balls}%5D+AND+Strikes+%3D+%5B{strikes}%5D+AND+Inning+%3D+%5B{inning}%5D+AND+PlayerId+%3D+%5B{batter}%5D+AND+PitchType+%3D+%5B%22{pitch_type}%22%5D+Order+By+Timestamp+DESC"

FILM_ROOM_SEARCH_COLUMNS: set[str] = {
    "pitcher",
    "batter",
    "pitch_type",
    "inning",
    "inning_top_bot",
    "outs_when_up",
    "balls",
    "strikes",
    "outs",
}


def search_mlb_film_room(
    pitch_row_dict: dict,
    date: datetime.datetime,
    prefix: Optional[str] = None,
) -> str:
    """hacks the mlb film room search url to find the video of a specific pitch"""
    year = date.year
    if prefix is None:
        print(pitch_row_dict)
        return FILM_ROOM_ROOT_URL.format(
            **pitch_row_dict, year=year, date=date.strftime("%Y-%m-%d")
        )

    prev_row_dict = {
        key.replace(prefix, ""): value
        for key, value in pitch_row_dict.items()
        if prefix in key
        and key[len(prefix) :] in FILM_ROOM_SEARCH_COLUMNS
        or key in FILM_ROOM_SEARCH_COLUMNS
    }
    pprint(prev_row_dict)
    return FILM_ROOM_ROOT_URL.format(
        **prev_row_dict, year=year, date=date.strftime("%Y-%m-%d")
    )


if __name__ == "__main__":
    # test case from this tweet: https://x.com/_holmj_/status/1829562821245559025
    link = search_mlb_film_room(
        pitch_row_dict={
            "pitcher": 687924,
            "batter": 680474,
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

    prev_link = search_mlb_film_room(
        pitch_row_dict={
            "prev_pitcher": 687924,
            "prev_batter": 680474,
            "prev_pitch_type": "SI",
            "prev_inning": 2,
            "prev_inning_top_bot": "TOP",
            "prev_outs": 0,
            "prev_balls": 1,
            "prev_strikes": 0,
        },
        date=datetime.datetime(2024, 8, 29),
        prefix="prev_",
    )
    print(prev_link)
