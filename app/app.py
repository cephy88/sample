


from flask import Flask, request, render_template, redirect, url_for
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb+srv://admin:admin@samplecluster.cyfvrvo.mongodb.net/db?retryWrites=true&w=majority"

mongo = PyMongo(app)

print(mongo.db)  # add this line
users = mongo.db.users.find().sort("_id", DESCENDING)


@app.route('/')
def users():
    users = mongo.db.users.find().sort("_id", DESCENDING)
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        if request.form['name'] and request.form['email']:
            user = {
                "name": request.form['name'],
                "email": request.form['email']
            }
            mongo.db.users.insert_one(user)
    return redirect(url_for('users'))

@app.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    if request.method == 'POST':
        if request.form['name'] and request.form['email']:
            user = {
                "name": request.form['name'],
                "email": request.form['email']
            }
            mongo.db.users.update_one({'_id': ObjectId(user_id)}, {"$set": user})
    return redirect(url_for('users'))

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('users'))

if __name__ == "__main__":
    app.run(debug=True)
