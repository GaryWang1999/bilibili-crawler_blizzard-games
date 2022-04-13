from general import *
from infoFinder import *
import csv

field_names = ['game_name', 'title', 'view', 'dm',
               'like', 'coin', 'collect', 'share',
               'upload_date', 'url']

class Spider:

    project_name = ''
    queue_file = ''
    crawled_file = ''
    url_list = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, game_name, url_list):
        Spider.project_name = project_name
        Spider.game_name = game_name
        Spider.url_list = url_list
        Spider.queue_file = Spider.project_name + '/' + game_name + '_queue.txt'
        Spider.crawled_file = Spider.project_name + '/' + game_name + '_crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.game_name, Spider.url_list)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.game_name, Spider.url_list)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, game_name, url_list):
        path = "data/" + game_name + ".csv"
        f = open(path, 'a', newline='')
        writer = csv.DictWriter(f, fieldnames= field_names)
        writer.writeheader()

        for url in url_list:
            if url not in Spider.crawled:
                print(thread_name + ' now crawling ' + url)
                print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
                # crawl information
                info = getInfo(url)
                info['game_name'] = game_name
                info['url'] = url

                try:
                    writer.writerow(info)
                except:
                    print("A small error encountered, but no worry, let's just skip it")
                    pass

                # update files
                Spider.queue.remove(url)
                Spider.crawled.add(url)
                Spider.update_files()
        f.close()
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

