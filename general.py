import os

#Each website we crawl is a project
def create_project_directory(directory):
    if not os.path.exists(directory):
        print('creating project', directory)
        os.makedirs(directory)

def write_file(path,data):
    file = open(path, 'w')
    file.write(data)
    file.close()

def append_file(path,data):
    file = open(path, 'a')
    file.write(data+'\n')
    file.close()

def delete_content_file(path):
    with open(path, 'w'):
        pass

#read file and convert to set
def file_to_set(file_name):
    result = set()
    file = open(file_name, 'r');
    for line in file:
        result.add(line.strip('\n'))
    return result
def set_to_file(data_set, file):
    delete_content_file(file)
    for data in sorted(data_set):
        append_file(file, data)


def create_data_file(project_name, base_url):
    queue = project_name+'/queue.txt'
    crawled = project_name+'/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

def delete_files(project_name):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if os.path.isfile(queue):
        os.remove(queue)
    if os.path.isfile(crawled):
        os.remove(crawled)
#create_data_file('test_directory', 'https://www.worldometers.info/coronavirus/')

#create_project_directory('test_directory')