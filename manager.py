from flask import Flask, render_template, url_for

manager = Flask(__name__)

org_info_parse = "Random"

@manager.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html', org=org_info_parse)

if __name__ == '__main__':
    manager.run(debug=True)
