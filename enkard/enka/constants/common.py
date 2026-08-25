from typing import Final

CN_UID_PREFIXES: Final[tuple[str, ...]] = ("1", "2", "5")
DEFAULT_TIMEOUT: Final[int] = 5  # Seconds before API request times out

GI_API_URL: Final[str] = "https://enka.network/api/uid/{}"
PROFILE_API_URL: Final[str] = "https://enka.network/api/profile/{}/hoyos/{}/builds/"
