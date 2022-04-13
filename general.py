import os

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

# Create queue and crawled files (if not created)
def create_data_files(project_name, game_name, url_list):
    queue_file_name = game_name + '_queue.txt'
    queue = os.path.join(project_name , queue_file_name)
    crawled_file_name = game_name + '_crawled.txt'
    crawled = os.path.join(project_name, crawled_file_name)
    if not os.path.isfile(queue):
        write_file(queue, url_list)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        for item in data:
            f.write(item)
            f.write('\n')

# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")