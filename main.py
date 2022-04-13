import threading
from queue import Queue
from spider import Spider
from general import *

PROJECT_NAME = 'blizzard_games'

NUMBER_OF_THREADS = 5
queue = Queue()

#### Getting all urls ready
url_files = os.listdir('url_list')
url_list = []
for url_file in url_files:
    urls = []
    path = 'url_list/' + url_file
    with open(path) as file:
        lines = file.readlines()
        print('Reading ' + str(len(lines)) + " urls from " + url_file)
        for line in lines:
            line = line.replace('\n', '')
            urls.append(line)
    url_list.append(urls)

GAME_NAMES = ['X战警前传：金刚狼', '使命召唤', '冰封王座', '变形金刚2：卷土重来',
              '吉他英雄', '命运2', '命运战士', "天诛系列", '星际争霸',
              '暗黑破坏神', '暗黑破坏神II', '炉石传说', '虐杀原形',
              '风暴英雄', '魔兽世界', '魔兽争霸']

#### data folder
create_project_dir('data')


# It is kinda strange here
# I want to make the program multi-threaded
# but for webdriver, should it open up a bunch of browsers?
# I am leaving this code chunks over here for potential future update

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

for n in range(len(GAME_NAMES)):
    print(n)
    queue_file = PROJECT_NAME + '/' + GAME_NAMES[n] +'_queue.txt'
    crawled_file = PROJECT_NAME + '/' + GAME_NAMES[n] +'_crawled.txt'
    Spider(PROJECT_NAME, GAME_NAMES[n], url_list[n])
    create_workers()
    crawl()
