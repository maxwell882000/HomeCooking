from application import app
from .date import convert_utc_to_asia_tz
from application.resources import strings


@app.template_filter()
def datetime(value, date_format='%d.%m.%Y %H:%M:%S', convert_from_utc=False):
    if convert_from_utc:
        date = convert_utc_to_asia_tz(value)
    else:
        date = value
    return date.strftime(date_format)


@app.template_filter()
def shipping_method(value):
    return strings.from_order_shipping_method(value, 'ru')


@app.template_filter()
def payment_method(value):
    return strings.from_order_payment_method(value, 'ru')


@app.template_filter()
def price(value):
    return '{0:,}'.format(value).replace(',', ' ')
