#/usr/bin/env python3

import asyncio
import aiohttp
import logging


from bs4 import BeautifulSoup

_debug = False

def log(msg, level='debug'):
    logging.basicConfig(level=logging.DEBUG if globals()['_debug'] else logging.INFO, handlers=[logging.StreamHandler()])
    logger = logging.getLogger()
    getattr(logger, level if hasattr(logger, level) else 'debug')(str(msg))



class WebScraper(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1;+http://www.google.com/bot.html)"
    }

    def __init__(self, urls) -> None:
        self.urls = urls
        self.all_data = []
        self.master_dict = {}
        asyncio.run(self.main())


    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                text = await response.text()
                title_tag = await self.extract_title_tag(text)
                log('returning text: ')
                return text, url, title_tag
        except Exception as e:
            log('Error Occured: ' + str(e))
            return None

    async def extract_title_tag(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return soup.title.text
        except Exception as e:
            log(f'{self.extract_title_tag.__str__} Error occured: {str(e)}')
            return None


    async def main(self) -> None:
        tasks = []
        async with  aiohttp.ClientSession(headers=self.headers) as session:
            for url in self.urls:
                log(f'Making Connection to url: {url}...')
                tasks.append(self.fetch(session, url))
            
            htmls = await asyncio.gather(*tasks)

            self.all_data.extend(htmls)

            for html in htmls:
                if html is not None:
                    url = html[1]
                    self.master_dict[url] = {'Raw Html': html[0], 'Title': html[2]}
                else:
                    continue
    

if __name__ == '__main__':
    log('Running webscraper....', 'info')
    urls = ['https://understandingdata.com']
    scraper = WebScraper(urls=urls)
    print('\n')
    print('Title: ', scraper.master_dict[urls[0]]['Title'])