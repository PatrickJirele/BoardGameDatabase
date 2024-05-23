import flask
from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SECRET_KEY'] = 'secretKey'
db = SQLAlchemy(app)


class boardgames(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20))
    Price = db.Column(db.Integer)
    Players = db.Column(db.String(10))
    PlayTime = db.Column(db.Integer)
    Link = db.Column(db.String(200))


@app.route('/sort', methods=['POST'])
def sort_games():
    column = request.form.get('column')
    order = request.form.get('order', 'asc')

    sort_column = getattr(boardgames, column)
    if order == 'asc':
        results = boardgames.query.order_by(sort_column).all()
    else:
        results = boardgames.query.order_by(sort_column.desc()).all()

    games = [{'ID': game.ID, 'Name': game.Name, 'Price': game.Price, 'Players': game.Players, 'PlayTime': game.PlayTime,
              'Link': game.Link} for game in results]
    return jsonify(games)


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    if search_term:
        results = boardgames.query.filter(boardgames.Name.ilike(f'%{search_term}%')).all()
    else:
        results = boardgames.query.all()
    games = [{'ID': game.ID, 'Name': game.Name, 'Price': game.Price, 'Players': game.Players, 'PlayTime': game.PlayTime,
              'Link': game.Link} for game in results]
    return jsonify(games)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        Name = request.form['Name']
        Price = request.form['Price']
        Players = request.form['Players']
        PlayTime = request.form['PlayTime']
        Link = request.form['Link']

        temp = boardgames(Name=Name,
                          Price=Price,
                          Players=Players,
                          PlayTime=PlayTime,
                          Link=Link
                          )

        db.session.add(temp)
        db.session.commit()
        games = boardgames.query.all()
        return render_template("home.html", games=games)

    elif request.method == 'GET':
        return render_template('create.html')


@app.route('/delete/<gameID>', methods=['POST'])
def delete(gameID):
    if request.method == 'POST':
        results = boardgames.query.filter_by(ID=gameID).first()
        db.session.delete(results)
        db.session.commit()
        games = boardgames.query.all()
        return render_template("home.html", games=games)


@app.route('/update/<gameID>', methods=['GET', 'POST'])
def update(gameID):
    if request.method == 'POST':
        results = boardgames.query.filter_by(ID=gameID).first()
        Name = request.form['Name']
        Price = request.form['Price']
        Players = request.form['Players']
        PlayTime = request.form['PlayTime']
        Link = request.form['Link']

        results.Name = Name
        results.Age = Price
        results.Players = Players
        results.PlayTime = PlayTime
        results.Link = Link

        db.session.commit()

        games = boardgames.query.all()
        return render_template("home.html", games=games)
    elif request.method == 'GET':
        game = boardgames.query.filter_by(ID=gameID).first()
        return render_template("update.html", ID=gameID, game=game)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        games = boardgames.query.all()
        return render_template("home.html", games=games)
    elif request.method == 'POST':
        # get info from search bar
        games = boardgames.query.all()
        return render_template("home.html", games=games)


if __name__ == '__main__':
    app.run()
