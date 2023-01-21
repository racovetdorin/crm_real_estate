import base64
import hashlib
import hmac

class ImgProxy:

    def __init__(self, key, salt):
        self._key = bytes.fromhex(key)
        self._salt = bytes.fromhex(salt)

    def generate(self, url, resize, width, height, gravity, enlarge, extension):
        b64_url = base64.urlsafe_b64encode(str.encode(url)).rstrip(b'=').decode()

        path = f'/{resize}/{width}/{height}/{gravity}/{enlarge}/{b64_url}.{extension}'

        sha256_hmac = hmac.new(self._key, self._salt + str.encode(path), digestmod=hashlib.sha256)

        protection = base64.urlsafe_b64encode(sha256_hmac.digest()).rstrip(b'=').decode()

        return f'/{protection}{path}'

    def generate_advanced(self, url, resize, watermark, quality, extension):
        b64_url = base64.urlsafe_b64encode(str.encode(url)).rstrip(b'=').decode()

        resize = ':'.join(resize)
        resize = f'resize:{resize}'

        watermark = ':'.join(watermark)
        watermark = f'watermark:{watermark}'
        quality = f'quality:{quality}'

        processing_options = f'{resize}/{watermark}/{quality}'

        path = f'/{processing_options}/{b64_url}.{extension}'

        sha256_hmac = hmac.new(self._key, self._salt + str.encode(path), digestmod=hashlib.sha256)
        protection = base64.urlsafe_b64encode(sha256_hmac.digest()).rstrip(b'=').decode()

        return f'/{protection}{path}'