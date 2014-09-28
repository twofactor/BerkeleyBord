from flask import Flask, request, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)
	score = db.Column(db.Integer())

	def __init__(self, message, pub_date=None):
		self.message = message
		self.score = 1
		if pub_date is None:
			pub_date = datetime.utcnow()
		self.pub_date = pub_date

	def __repr__(self):
		return '<message %r>' % self.message

posts = Post.query.order_by(desc(Post.id)).all()
swags = swags = Post.query.order_by(desc(Post.score)).all()


def db_add_post(post_text):
	newPost = Post(post_text)
	db.session.add(newPost)
	db.session.commit()

def db_increase_score(post_id):
	this_post = Post.query.filter_by(id=post_id).first()
	this_post.score += 1
	db.session.add(this_post)
	db.session.commit()

@app.route("/api/bbord", methods=["POST"])
def receive_message():
	db_add_post(request.form["message"])
	posts = Post.query.order_by(desc(Post.id)).all()
	swags = Post.query.order_by(desc(Post.score)).all()
	return render_template('index.html', posts = posts, swag = swags)

@app.route("/upvote/<postId>")
def upvotafier(postId):
	db_increase_score(postId)
	posts = Post.query.order_by(desc(Post.id)).all()
	swags = Post.query.order_by(desc(Post.score)).all()
	return render_template('index.html', posts = posts, swag = swags)


@app.route("/")
def hello():
	posts = Post.query.order_by(desc(Post.id)).all()
	swags = Post.query.order_by(desc(Post.score)).all()
	return render_template('index.html', posts = posts, swag = swags)

if __name__ == "__main__":
    app.run(debug=True)