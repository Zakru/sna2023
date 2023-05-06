from urllib.request import urlopen
import os


def post_pages():
    yield 'https://www.city-data.com/forum/health-wellness/3245374-have-you-had-covid-vaccine-side.html'
    for i in range(2, 54):
        yield f'https://www.city-data.com/forum/health-wellness/3245374-have-you-had-covid-vaccine-side-{i}.html'


try:
    os.mkdir('pages')
except:
    pass

for i, page_url in enumerate(post_pages()):
    with open(f'pages/page-{i+1}.html', 'wb') as f:
        f.write(urlopen(page_url).read())
