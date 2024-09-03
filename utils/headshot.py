from typing import Optional
import requests
from PIL import Image
from io import BytesIO

__all__ = ["get_player_headshot"]

HEADSHOT_BASE_URL = "https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_426,q_auto:best/v1/people/{player_mlbam_id}/headshot/67/current"


def get_player_headshot(player_mlbam_id: str) -> Image.Image:
    """
    Scrapes the players headshot with the given mlbam id from the
    HEADSHOT_BASE_URL url. This function both returns the numpy array
    of image data from the players headshot as well as saves the image
    to the assets directory under the name "assets/profile_pic.jpg"

    @params
        player_mlbam_id: string of the players mlbam id.

    @return
        PIL Image.Image object of the players headshot.
    """

    url = HEADSHOT_BASE_URL.format(player_mlbam_id=player_mlbam_id)
    r: Optional[requests.models.Response] = None
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get player headshot image from {url}\nerror: {e}")

    if r.status_code != 200:
        raise ValueError(f"Failed to get player headshot image from {url}")
    return Image.open(BytesIO(r.content))


if __name__ == "__main__":
    TEST_PLAYER_ID = "545361"  # Mike Trout
    headshot = get_player_headshot(TEST_PLAYER_ID)
    headshot.show()
