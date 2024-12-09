import random
from collections import Counter
import string
import threading
import multiprocessing
import os
import time
from collections import defaultdict

def text_file(file_name, count_lines, count_word=10):
    words = ["".join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) for _ in range(100)]
    with open(file_name, "w") as file:
        for _ in range(count_lines):
            line = " ".join(random.choices(words, k=count_word))
            file.write(line + "\n")

def count_words(file_name):
    word_count = {}
    translator = str.maketrans('', '', string.punctuation)  
    with open(file_name, 'r') as file:
        for line in file:
            words = line.strip().split()
            for word in words:
                word = word.translate(translator).lower() 
                word_count[word] = word_count.get(word, 0) + 1
    return word_count


def count_words_chunk(file_name, start, end, result_queue):
    local_word_count = defaultdict(int)
    with open(file_name, 'r') as file:
        file.seek(start)
        while file.tell() < end:
            line = file.readline()
            words = line.strip().split()
            for word in words:
                word = word.strip(string.punctuation).lower()
                local_word_count[word] += 1
    result_queue.put(local_word_count)

def count_words_multithreaded(file_name, count_threads):
    word_count = Counter()

    def count_words_chunk(start, end):
        local_word_count = Counter()
        with open(file_name, 'r') as file:
            file.seek(start)
            while file.tell() < end:
                line = file.readline()
                words = line.strip().translate(str.maketrans('', '', string.punctuation)).lower().split()
                local_word_count.update(words)
        word_count.update(local_word_count)

    file_size = os.path.getsize(file_name)
    chunk_size = file_size // count_threads
    threads = []
    for i in range(count_threads):
        start = i * chunk_size
        end = start + chunk_size if i < count_threads - 1 else file_size
        thread = threading.Thread(target=count_words_chunk, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return dict(word_count)

def count_words_multiprocessing(file_name, count_processes):
    file_size = os.path.getsize(file_name)
    chunk_size = file_size // count_processes
    processes = []
    result_queue = multiprocessing.Queue()

    for i in range(count_processes):
        start = i * chunk_size
        end = start + chunk_size if i < count_processes - 1 else file_size
        process = multiprocessing.Process(target=count_words_chunk, args=(file_name, start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    word_count = defaultdict(int)
    while not result_queue.empty():
        local_word_count = result_queue.get()
        for word, count in local_word_count.items():
            word_count[word] += count

    return dict(word_count)


if __name__ == "__main__":
    file_name = 'text_file.txt'
    text_file(file_name, count_lines=1000, count_word=15)

    start = time.time()
    count_words(file_name)
    end = time.time()
    print(f"{end - start} seconds (1-threaded)")

    start = time.time()
    count_words_multithreaded(file_name, count_threads=4)
    end = time.time()
    print(f"{end - start} seconds (Multithreaded)")


    start = time.time()
    count_words_multiprocessing(file_name, count_processes=4)
    end = time.time()
    print(f"{end - start} seconds (Multiprocessing)")
