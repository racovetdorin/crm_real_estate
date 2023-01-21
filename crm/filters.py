from .imgproxy import ImgProxy
from .settings.remaxmd import STORAGE_DNS
from .settings.remaxmd import IMG_PROXY_KEY
from .settings.remaxmd import IMG_PROXY_SALT
from .settings.remaxmd import IMG_PROXY_HOST_999, IMG_PROXY_HOST


def get_details_medium_watermarked_thumbnail_url(image_url, host=False):
    image_url = f'{STORAGE_DNS}/{image_url}'
    img_proxy = ImgProxy(IMG_PROXY_KEY, IMG_PROXY_SALT)
    resize = 'fit'
    width = '1280'
    height = '999999999999'  # impossible size for imgproxy algorithm to fit correctly
    enlarge = '1'
    extend = '0'
    extension = 'jpeg'
    watermark_opacity = '0.9' if host else '0.6'
    watermark_position = 'ce'
    x_offset = '0'
    y_offset = '0'
    scale = '0.35'
    quality = 70

    resize = (resize, width, height, enlarge, extend)
    watermark = (watermark_opacity, watermark_position, x_offset, y_offset, scale)

    thumbnail_path = img_proxy.generate_advanced(image_url, resize, watermark, quality, extension)

    host = IMG_PROXY_HOST if host else IMG_PROXY_HOST_999
    
    return host + thumbnail_path