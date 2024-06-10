from flask import Flask, jsonify, render_template
from avltree import AVLTree
import random
from blackfire import probe

app = Flask(__name__)


@app.route('/space_usage', methods=['GET'])
def space_usage_test():
    probe.initialize()
    probe.enable()

    tree = AVLTree()
    n = 1000
    for _ in range(n):
        tree.insert_key(random.randint(0, 10000))

    probe.end()
    return jsonify(size=tree.get_size(), nodes=tree.node_count)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
