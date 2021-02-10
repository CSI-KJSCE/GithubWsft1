from flask import Flask
from flask import request, jsonify, render_template,redirect,url_for
import os
import json
import sqlite3


app = Flask(__name__)


@app.route('/')
def test():
    path = 'data/'
    files = [s for s in os.listdir(path)
         if os.path.isfile(os.path.join(path, s))]
    files.sort(key=lambda s: os.path.getmtime(os.path.join(path, s)))
    # print(files)
    db = sqlite3.connect('sys/db/likes.db')
    cur=db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS likes(likes INT  DEFAULT 0,name char(200) NOT NULL)")
    # cur.execute("DELETE FROM likes")
    for filename in files:
        filename=filename[:-5]
        # print(filename)
        cur.execute("SELECT name FROM likes")
        existing_files=cur.fetchall()
        existing_files=[name[0] for name in existing_files]
        print(existing_files)
        if not filename in existing_files:
            cur.execute("INSERT INTO likes (name) values('{}')".format(filename))
    db.commit()
    db.close()
    # print(files)
    result = []
    c=0
    for file in files:
        with open("data/"+file, 'r') as f:
            try:
                json_data = json.load(f)
                json_data['id'] = c
                c+=1
                # print("json = ",json_data)
                result.append(json_data)
            except Exception as e:
                print(e)
    # print("results = ",result)
    return render_template('index.html', results=result)

@app.route('/likes')
def like():
    name=request.args.get('name')
    print(name)
    db=sqlite3.connect('sys/db/likes.db')
    cur=db.cursor()
    cur.execute('UPDATE likes SET likes = likes + 1 WHERE name ="{}"'.format(name))
    db.commit()
    db.close()
    return jsonify({'success':'True'})

app.run()