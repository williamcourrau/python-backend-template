import requests
from requests.exceptions import RequestException, Timeout
from app.config.logging import get_logger

logger = get_logger(__name__)


class UrlConnectionService:
    """
        Service responsible for retrieving raw candidate data from an external URL.

        This class abstracts HTTP communication and provides:
        - Timeout handling
        - HTTP error handling
        - User-friendly error messages for non-technical users (e.g. HR)
        - Detailed logging for debugging and monitoring

        It does NOT parse or validate the returned data.
    """
    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    def fetch(self) -> str:
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()

            if not response.text:
                logger.warning("Empty response received from URL: %s", self.url)
                raise ValueError("There was no information found for candidate(s). Please try again and if the issue persists, contact support.")

            return response.text

        except Timeout as e:
            logger.error("Timeout while fetching URL %s", self.url, exc_info=e)
            raise RuntimeError(
                "We were unable to retrieve the candidate information because the "
                "external system took too long to respond. Please try again later."
            )

        except RequestException as e:
            logger.error("Request error while fetching URL %s", self.url, exc_info=e)
            raise RuntimeError(
                "We couldn’t retrieve the candidate information at this time. "
                "The external system may be temporarily unavailable. "
                "Please try again later or contact support if the issue continues."
            )

        except Exception as e:
            logger.exception("Unexpected error while fetching URL %s", self.url)
            raise RuntimeError(
                "An unexpected issue occurred while retrieving candidate information. "
                "No data was lost. Please try again later."
            )
