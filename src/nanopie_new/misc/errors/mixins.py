from abc import ABC, abstractmethod
from typing import Dict

class HTTPErrorMixIn(ABC):
    """
    """
    @property
    def http_status_code(self) -> int:
        """
        """
        if getattr(self, '_http_status_code'):
            return self._http_status_code
        else:
            raise 500

    @http_status_code.setter
    def http_status_code(self, http_status_code: int):
        """
        """
        self._http_status_code = http_status_code

    @property
    def extra_headers(self) -> Dict:
        """
        """
        headers = { 'Content-Type': 'text/html; charset=UTF-8' }
        if getattr(self, '_extra_headers'):
            return headers.update(self._extra_headers)
        else:
            return headers
    
    @extra_headers.setter
    def extra_headers(self, extra_headers: Dict):
        """
        """
        self._extra_headers = extra_headers

    @property
    def body_text(self) -> str:
        """
        """
        if getattr(self, '_body_text'):
            return self._body_text
        else:
            return ''

    @body_text.setter
    def body_text(self, body_text: str):
        """
        """
        self._body_text = body_text
