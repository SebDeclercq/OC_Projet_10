from django import template

register = template.Library()


@register.filter
def resize_img(img_url: str, length: str = '400') -> str:
    return img_url.replace('.full.', f'.{length}.')
