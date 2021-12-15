# app.py

# Required imports
import os
import atexit
import feed_data_to_firebase
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from apscheduler.schedulers.background import BackgroundScheduler
from collections import OrderedDict

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('car')


def routine_update_db():
    """
        for updating records in the firebase
    """
    feed_data_to_firebase.update_db()
    
# Sceduled process to update db every 24 hours
scheduler = BackgroundScheduler()
scheduler.add_job(func=routine_update_db, trigger="interval", seconds=86400)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/add', methods=['POST'])
def create():
    """
        create new data this was for testing for connectivity
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/getAllItems', methods=['GET'])
def get_all_items():
    """
        get all items
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/getItem', methods=['GET'])
def getItem():
    """
            get item example: Request Body ={"id": 1}
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/view', methods=['GET'])
def view():
    """
        for table view data in the html
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            # return jsonify(todo.to_dict()), 200
            return render_template("view.html",view = todo.to_dict())
        else:
            all_todos = [OrderedDict(sorted(doc.to_dict().items())) for doc in todo_ref.stream()]
            # return jsonify(all_todos), 200
            return render_template("view.html",view = all_todos)
    except Exception as e:
        return f"An Error Occured: {e}"
        
@app.route('/graphView', methods=['GET'])
def graph_view():
    """
        graph view 
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            # return jsonify(todo.to_dict()), 200
            return render_template("view.html",view = todo.to_dict())
        else:
            all_todos = [OrderedDict(sorted(doc.to_dict().items())) for doc in todo_ref.stream()]
            temp = all_todos.copy()
            list_temp = []
            v = 0
            for i in all_todos:
                i.pop('Aug')
                i.pop('Apr')
                i.pop('Category')
                i.pop('Dec')
                i.pop('Feb')
                i.pop('Jan')
                i.pop('Jul')
                i.pop('Jun')
                i.pop('Mar')
                i.pop('May')
                i.pop('Nov')
                i.pop('Oct')
                i.pop('Sep')
                i.pop('id')
            list_temp.append(['Model', 'Sumofsales'])
            for j in all_todos:
                list_temp.append([j['Model'], j['Sumofsales']])
                        
            # print(list_temp)
            # return jsonify(all_todos), 200
            return render_template("graph.html",graph = list_temp)
    except Exception as e:
        return f"An Error Occured: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)