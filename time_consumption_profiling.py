# time_consumption_profiling.py

from flask import Flask, jsonify, render_template
from avltree import AVLTree
import time
import random
from blackfire import probe

app = Flask(__name__)

def measure_time(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return end - start, result

@app.route('/time_consumption', methods=['GET'])
def time_consumption_test():
    probe.initialize()
    probe.enable()

    tree = AVLTree()
    n = 1000
    keys = list(range(n))
    random.shuffle(keys)

    # Insertions
    insert_times = []
    for key in keys:
        insert_time, _ = measure_time(tree.insert_key, key)
        insert_times.append(insert_time)

    # Searching
    search_times = []
    for key in keys:
        search_time, _ = measure_time(tree.search_key, key)
        search_times.append(search_time)

    # Deletions
    delete_times = []
    for key in keys:
        delete_time, _ = measure_time(tree.delete_key, key)
        delete_times.append(delete_time)

    probe.end()

    return jsonify(
        avg_insertion_time=sum(insert_times) / n,
        avg_search_time=sum(search_times) / n,
        avg_deletion_time=sum(delete_times) / n
    )

@app.route('/')
def index():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)