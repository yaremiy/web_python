from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
import bs4
from datetime import datetime


def application(environ, start_response):

    text = open('index.html', encoding='utf-8').read()
    soup = bs4.BeautifulSoup(text)
    sum_label = soup.find('label', attrs={'class': 'sum'})
    time_label = soup.find('label', attrs={'class': 'time'})

    if environ['CONTENT_LENGTH']:
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(
            request_body_size).decode("utf-8")
        d = parse_qs(request_body)

        try:
            x = int(d.get('text1')[0])
            y = int(d.get('text2')[0])
            sum = x + y
        except:
            sum = "Error"

        sum_label.string = f'Sum = {sum}'
        time_label.string = f'Time = {datetime.now().strftime("%H:%M:%S")}'

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(str(soup))))
    ]
    start_response(status, response_headers)
    return [bytes(str(soup), 'utf-8')]


httpd = make_server(
    'localhost',
    8051,
    application
)

httpd.serve_forever()
