import threading
from queue import Queue
from web_crawler.spider import Spider
from web_crawler.domain import *
from web_crawler.general import *
from web_crawler.extract_data import *

PROJECT_NAME = 'covid'
HOME_PAGE = 'https://www.worldometers.info/coronavirus/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

queue =Queue()
Spider(PROJECT_NAME,HOME_PAGE,DOMAIN_NAME)

#create workers
def create_workers():
    for rng in range(NUMBER_OF_THREADS):
        t = threading.Thread(target= work)
        t.daemon = True
        t.start()

#next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.currentThread().name, url)
        queue.task_done()

#each link is a job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

#check items in queue
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    #print(f'queue_links:::',queue_links)
    if len(queue_links) > 0:
        for link in queue_links:
            crawl_data_from_link(link)
        print('queue_links',queue_links)
        print(f'{len(queue_links)} in the queue')
        create_jobs()


create_workers()
crawl()