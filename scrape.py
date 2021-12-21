import requests
from bs4 import BeautifulSoup
import pprint

# res = requests.get("https://news.ycombinator.com/news?p=")
URL = 'https://news.ycombinator.com/news?p='
number_of_pages = 10

# soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.select('#score_29568625'))   # refer to css selectors
# print(soup.select('.score'))


def get_info(url, page_num):
    # getting the url and parsing the texts from the url on specific page
    res = requests.get(f'{url}{page_num}')
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.titlelink')
    subtext = soup.select('.subtext')
    return links, subtext


def sort_by_votes(hn):
    # sorts through the mega list and order them by highest to lowest votes.
    return sorted(hn, key=lambda k: k['Votes'], reverse=True)


def create_custom_hn(links, subtext, min_votes):
    """Sorting and filtering through the hackernews articles to only get the articles with more than required votes

    Args:
        links ([li]): links and title of each article
        subtext ([li]): subtext(to get the votes, can't use votes as sometimes there's no votes)
        votes ([int]): minimum amount of votes to be appended to list

    Returns:
        li: Full sorted list of the articles with the votes and links attached
    """
    hn = []
    for i, item in enumerate(links):

        title = links[i].getText()
        # Some articles might have corrupted links
        href = links[i].get('href', None)
        votes = subtext[i].select('.score')  # Get the votes of each article
        if len(votes):
            points = int(votes[0].getText().replace(' points', ''))
            if points > min_votes:
                hn.append({'Title': title, 'link': href, 'Votes': points})
    return hn


# pprint.pprint(create_custom_hn(links, subtext))

def main():
    mega_list = []
    for i in range(1, number_of_pages):
        links, subtext = get_info(URL, i)
        mega_list += create_custom_hn(links, subtext, 500)
    pprint.pprint(sort_by_votes(mega_list))


if __name__ == '__main__':
    main()
