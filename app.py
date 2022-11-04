from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e3aed434bbcc327d1a6eb4a645e8eb4673ce6ec9bf3145ce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_db_dg98_user:0kaZ3dWd8KfJBSvuaX9RtnV7bnynWrRt@dpg-cd99q81a6gdv16a31ivg-a/todo_db_dg98'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

us_id = 0

class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    info = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Postss', backref='poster',cascade='all, delete')




    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

class Postss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
    # Foreign Key To Link Lists (refer to primary key of the user)
    poster_id = db.Column(db.Integer, db.ForeignKey('lists.id'))



# Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

class Artiklar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    info = db.Column(db.String(100))
    category = db.Column(db.String(100))

    def __repr__(self):
        return f'<Artikel: {self.name}>'

db.create_all()

class ArtikelForm(FlaskForm):
    name = StringField("Namn", validators=[DataRequired()])
    info = StringField("Info")
    category = StringField("Kategori")

    submit = SubmitField("Lägg till")

class PostForm(FlaskForm):
    name = StringField("Namn", validators=[DataRequired()])
    info = StringField("Info")
    category = StringField("Kategori")

    submit = SubmitField("Lägg till")


class ListForm(FlaskForm):
    name = StringField("Namn", validators=[DataRequired()])
    info = StringField("Info")
    category = StringField("Kategori")
    submit = SubmitField("Lägg till")

@app.route('/')
def index():
    our_lists = db.session.query(Lists).all()
    return render_template("index.html", our_lists=our_lists)
   # return render_template("index.html")


@app.route("/artiklar", methods=["GET", "POST"])
def artiklar():
    form = ArtikelForm()
    new_category=[]
    if request.method == "POST":
        # CREATE RECORD
        new_user = Artiklar(
            name=request.form["name"],
            info=request.form["info"],
            category=request.form["category"]
        )
        db.session.add(new_user)
        db.session.commit()

        all_artiklar = db.session.query(Artiklar).all()
        return redirect(url_for('artiklar',Artiklar=all_artiklar))

    artiklar_query = db.session.query(Artiklar).order_by(Artiklar.category)
   # category_list = db.session.query(Artiklar.category).all()
    category_list = db.session.query(Artiklar.category).order_by(Artiklar.category)

    list_of_values = category_list
    for item in list_of_values:
        if item not in new_category:
            new_category.append(item)

    return render_template("artiklar.html", Artiklar=artiklar_query, form=form, category_list=new_category)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name=None
    form = ListForm()
    if form.validate_on_submit():
        user = Lists.query.filter_by(info=form.info.data).first()
        print(Postss.poster_id)
        if user is None:
            lista= Lists(name=form.name.data, info=form.info.data, category=form.category.data)
            db.session.add(lista)
            db.session.commit()
#
        elif user is not None:
            flash("Email is not uniqe. Try again!")
            return redirect(url_for("add_user"))
        #name = form.name.data
        #print(user.email)
        us=form.name.data
        print(us)
#
        form.name.data = ''
        form.info.data = ''
        form.category.data = ''
        flash("Lista tillagd!")

    our_lists = Lists.query.order_by(Lists.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_lists=our_lists)

@app.route('/add_post/add/posts/<int:id>/<namn>', methods=['GET', 'POST'])
def add_post(id,namn):
    new_category = []
    global us_id
    form = PostForm()
    list_id = request.args.get('id')
    print(list_id)
    if form.validate_on_submit():
        poster = id
        print(id)
        post = Postss(name=form.name.data, info=form.info.data, category=form.category.data, poster_id=poster)

        # Clear The Form
        form.name.data = ''
        form.info.data = ''
        # form.author.data = ''
        form.category.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Post har lagts till!")

    us_id=id
    print(f"{us_id} us_id")
    #name = form.name.data
    posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done, Postss.poster_id).join(Lists).filter(id == Postss.poster_id).order_by(Postss.category).all()

    all_artiklar = db.session.query(Artiklar).order_by(Artiklar.category)

    category_list = db.session.query(Artiklar.category).order_by(Artiklar.category)

    list_of_values = category_list
    for item in list_of_values:
        if item not in new_category:
            new_category.append(item)
        # Redirect to the webpage
    return render_template("add_post.html",
                form=form,
                namn=namn,
                posts=posts,
                Artiklar=all_artiklar,
                category_list=new_category)

@app.route('/lista', methods=["GET", "POST"])

def lista():
    if request.method == "POST":
        # CREATE RECORD
        new_lista = Lists(
            name=request.form["name"],
            info=request.form["info"],
            category=request.form["category"]
        )
        db.session.add(new_lista)
        db.session.commit()

    our_lists = Lists.query.order_by(Lists.date_added)

    return render_template("index.html",our_lists=our_lists)

@app.route('/edit_lista/<int:id>', methods=['GET', 'POST'])
def edit_lista(id):
    form = ListForm()
    name_to_update = Lists.query.get(id)
    print(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.info = request.form['info']
        name_to_update.category = request.form['category']

        db.session.commit()

    return render_template("edit_list.html", form=form, name_to_update=name_to_update, id=id)

@app.route("/delete_all/<int:id>")
def delete_all(id):
    list_to_delete = db.session.query(Lists).filter(Lists.id == id).first()
    print(f"{id}del_id")
    print(f"{list_to_delete}del_id")
    db.session.delete(list_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete")
def delete():
   list_id = request.args.get('id')
   list_to_delete = Lists.query.get(list_id)
   db.session.delete(list_to_delete)
   print("deleted")
   db.session.commit()
   return redirect(url_for('index'))

@app.route("/delete_art")
def delete_art():
    artikel_id = request.args.get('id')

    # DELETE A RECORD BY ID
    art_to_delete = Artiklar.query.get(artikel_id)
    db.session.delete(art_to_delete)
    db.session.commit()
    return redirect(url_for('artiklar'))


@app.route('/delete_post/posts/<int:id>', methods=["GET", "POST"])
def delete_post(id):
    new_category = []
    global us_id
    form = PostForm()
    #name = form.name.data

    if request.method == "GET":
        post_to_delete = Postss.query.get(id)
        db.session.delete(post_to_delete)
        # Posts.query.filter_by(id=id).delete()
        db.session.commit()

        print("deleted")
        print(us_id)
        flash("Post raderad!")
        our_lists = db.session.query(Lists).get(us_id)
        namn = our_lists.name
        #all_artiklar = db.session.query(Artiklar).all()
        all_artiklar = db.session.query(Artiklar).order_by(Artiklar.category)
        category_list = db.session.query(Artiklar.category).order_by(Artiklar.category)
        list_of_values = category_list
        for item in list_of_values:
            if item not in new_category:
                new_category.append(item)
        # posts = db.session.query(Posts, Posts.id, Posts.name, Posts.info, Posts.category, Posts.done, Posts.poster_id).join(Lists).filter(id == Posts.poster_id).order_by(Posts.category).all()
        posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done, Postss.poster_id).join(
            Lists).filter(us_id == Postss.poster_id).order_by(Postss.category).all()
        return render_template("add_post.html", form=form, posts=posts, namn=namn, Artiklar=all_artiklar, category_list=new_category)

    else:

        poster = us_id
        post = Postss(name=form.name.data, info=form.info.data, category=form.category.data, poster_id=poster)

        # Clear The Form
        form.name.data = ''
        form.info.data = ''
        # form.author.data = ''
        form.category.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Post tillagd!")
        #name = form.name.data
        our_lists = db.session.query(Lists).get(us_id)
        namn = our_lists.name
        all_artiklar = db.session.query(Artiklar).all()
        # posts = db.session.query(Posts, Posts.id, Posts.name, Posts.info, Posts.category, Posts.done, Posts.poster_id).join(Lists).filter(id == Posts.poster_id).order_by(Posts.category).all()
        posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done, Postss.poster_id).join(
            Lists).filter(us_id == Postss.poster_id).order_by(Postss.category).all()

        return render_template("add_post.html", form=form, posts=posts, namn=namn, Artiklar=all_artiklar)

@app.route("/complete/<int:id>", methods=['GET', 'POST'])
def complete(id):
    form = PostForm()
    new_category = []
    if request.method == "GET":
        check = Postss.query.filter_by(id=id).first()
        print(check.done)
        check.done = not check.done
        print("true to false")
        print(check.done)
        db.session.commit()
        posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done, Postss.poster_id).join(
        Lists).filter(us_id == Postss.poster_id).order_by(Postss.category).all()

        all_artiklar = db.session.query(Artiklar).order_by(Artiklar.category)
        category_list = db.session.query(Artiklar.category).order_by(Artiklar.category)

        list_of_values = category_list
        for item in list_of_values:
            if item not in new_category:
                new_category.append(item)
        our_lists = db.session.query(Lists).get(us_id)
        namn = our_lists.name
        return render_template("add_post.html",posts=posts ,form=form, namn=namn, Artiklar=all_artiklar, category_list=new_category)
    else:
        poster = us_id
        post = Postss(name=form.name.data, info=form.info.data, category=form.category.data, poster_id=poster)

        # Clear The Form
        form.name.data = ''
        form.info.data = ''
        # form.author.data = ''
        form.category.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Post tillagd!")
        #name = form.name.data
        our_lists = db.session.query(Lists).get(us_id)
        namn = our_lists.name

        posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done,
                                 Postss.poster_id).join(
            Lists).filter(us_id == Postss.poster_id).order_by(Postss.category).all()
        all_artiklar = db.session.query(Artiklar).order_by(Artiklar.category)

        return render_template("add_post.html", form=form, posts=posts, namn=namn, Artiklar=all_artiklar)


@app.route("/complete_false/<int:id>", methods=['GET', 'POST'])
def complete_false(id):
    form = PostForm()
    new_category = []
    if request.method == "GET":
        not_check = Postss.query.filter_by(id=id).first()

        print(id)
        print(not_check.done)
        not_check.done = True
        print(not_check.done)
        print("false to true")
        db.session.commit()
        our_lists = db.session.query(Lists).get(us_id)
        namn = our_lists.name

        posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done, Postss.poster_id).join(
        Lists).filter(us_id == Postss.poster_id).order_by(Postss.category).all()
        all_artiklar = db.session.query(Artiklar).order_by(Artiklar.category)
        category_list = db.session.query(Artiklar.category).order_by(Artiklar.category)

        list_of_values = category_list
        for item in list_of_values:
            if item not in new_category:
                new_category.append(item)
        return render_template("add_post.html",posts=posts,form=form, namn=namn, Artiklar=all_artiklar, category_list=new_category)
    else:
        poster = us_id
        post = Postss(name=form.name.data, info=form.info.data, category=form.category.data, poster_id=poster)

        # Clear The Form
        form.name.data = ''
        form.info.data = ''
        # form.author.data = ''
        form.category.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Post tillagd!")
        #name = form.name.data
        our_lists = db.session.query(Lists).get(us_id)
        namn = our_lists.name

        posts = db.session.query(Postss, Postss.id, Postss.name, Postss.info, Postss.category, Postss.done,
                                 Postss.poster_id).join(
            Lists).filter(us_id == Postss.poster_id).order_by(Postss.category).all()
        all_artiklar = db.session.query(Artiklar).order_by(Artiklar.category)
        return render_template("add_post.html", form=form, posts=posts, namn=namn, Artiklar=all_artiklar)



@app.route('/posts/<int:id>/<name>')
def posts(id,name):
    print(name)

   #if id == post.poster_id:


   # posts = Posts.query(Posts.date_added).filter(id == Posts.poster_id)

    #posts = Posts.query(Posts.date_added).filter(post.poster_id == 2)
    #print(post.poster_id)
    #posts = Posts.query.filter_by(id == Posts.poster_id)
    #posts = session.query(Posts).filter(posts.name.like('K%')).all()
 #    posts = Posts.query.filter_by(Posts.poster_id = "Mat").all()
    #posts = Posts.query.filter_by((Posts.category = 'Mat')).first()

  #       posts = Posts.query.order_by(Posts.date_added).all()


    #posts = Posts.query.filter_by(id=2).all()


    #posts = Posts.query.filter_by(Posts.poster_id=id).first()

    #postid = post.poster_id
    #posts = Posts.query.get_or_404(id)
    #postid = Posts.poster_id
    posts = db.session.query(Postss, Postss.name, Postss.info, Postss.category).join(Lists).filter(id == Postss.poster_id).all()
    for post in posts:

#user = db.session.query(User, Role.index).join(Role).filter(User.email == form.email.data).first()

     return render_template('post.html', posts=posts, name=name)






if __name__ == '__main__':
    app.run(debug=False)
