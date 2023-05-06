from bs4 import BeautifulSoup
from urllib.request import urlopen
from typing import Generator
import pickle


def is_post(id: str):
    return id.startswith('post')


def is_post_message(id: str):
    return id is not None and id.startswith('post_message_')


def is_quote(tag):
    smallfont = tag.find('div', { 'class': 'smallfont' }, recursive=False)
    return smallfont is not None and smallfont.get_text() == 'Quote:'


def int_with_commas(t: str):
    return int(t.replace(',', ''))


post_data = []


for page_num in range(1, 54):
    with open(f'pages/page-{page_num}.html', 'rb') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    posts_div = soup.find('div', { 'id': 'posts' })

    for post in posts_div.find_all('div', { 'align': 'center' }):
        content = post.find('table', { 'id': is_post })
        [date_row, info_row, content_row] = content.find_all('tr', recursive=False)

        # Extract username
        username_link = info_row.find('a', { 'class': 'bigusername' })
        username = username_link.get_text()

        # Extract user info
        info_div = info_row.find('div', { 'class': 'smallfont' })
        info_rows = info_div.find_all('div', recursive=False)
        if len(info_rows) == 2:
            [info_post_row, info_rep_row] = info_rows
            info_location_row = None
        else:
            [info_location_row, info_post_row, info_rep_row] = info_rows

        location = None
        if info_location_row:
            location = info_location_row.get_text().strip().split(' ', 1)[1]

        post_parts = info_post_row.get_text().strip().split(' ')
        post_count = int_with_commas(post_parts[0])
        post_read = int_with_commas(post_parts[3])

        reputation = int_with_commas(info_rep_row.get_text().strip().split(' ', 1)[1])

        # Extract post content
        post_message = content_row.td.find('div', { 'id': is_post_message })
        post_text = post_message.get_text()

        post_quotes = []
        for quote in post_message.find_all(is_quote):
            quotee_name = quote.table.tr.td.div
            quotee_name = quotee_name and quotee_name.strong
            if quotee_name is not None:
                post_quotes.append(quotee_name.get_text())
        if len(post_quotes) > 0: print(username, post_quotes)
        post_data.append({
            'username': username,
            'location': location,
            'posts': post_count,
            'read': post_read,
            'reputation': reputation,
            'text': post_text,
            'quotes': post_quotes,
        })


print(post_data)


with open('dump.pickle', 'wb') as f:
    pickle.dump(post_data, f)
