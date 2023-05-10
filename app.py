from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Hello"

#@app.before_first_request
#def setup():
#    init_db()
    
# TODO: Fill in methods and routes
init_db()
#Login method that checks if username and password match an entry in the users database
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        uname = request.form["username"]
        pw = request.form["password"]
        print(uname)
        print(pw)
        user = db_session.query(User).where((User.username == uname) & (User.password == pw)).first()
        while user == None:
            return render_template("login.html")
        else:
            #sets the session username to username so we know who is logged in
            session["username"] = uname
            return redirect(url_for("home"))
#Queries for all of the posts that are regarding colleges that the user follows
@app.route("/mycolleges", methods=("GET", "POST"))
def mycolleges():
    if request.method == "GET":
        #Takes the first three college posts from colleges the user follows
        posts = db_session.query(Post).join(CollegesFollowed, Post.post_college == CollegesFollowed.college_name).where(CollegesFollowed.user_username == session["username"]).order_by(Post.timestamp.desc()).limit(3).all()
        print(posts)
        #returns a page with information from these first three posts
        return render_template('my-colleges.html', posts = posts)
    elif request.method == "POST":
        school = request.form["school"]
        body = request.form["body"]
        hash = request.form["hash"]

        #ensures the college that the user inputs exists
        check = db_session.query(College).where(school == College.name).first()
        #Given that it exists, it saves the information the user inputs such as tags and content, along with the username itself to an entry in the posts database where it can be accessed later
        if check is not None:
            p = Post(content = body, post_username = session["username"], post_college = school, timestamp = datetime.now())
            db_session.add(p)
            db_session.commit()
            post = db_session.query(Post).where(body == Post.content).first()
            hash = hash.split()
            for tag in hash:
                if db_session.query(Tag).where(tag == Tag.content).first() is None:
                    t = Tag(content = tag)
                    db_session.add(t)
                    db_session.commit()
                tagadded = db_session.query(Tag).where(tag == Tag.content).first()
                new_posttag = PostTag(tag_id = tagadded.id, post_id = post.id)
                db_session.add(new_posttag)
                db_session.commit()
            return redirect(url_for("mycolleges"))
                    

#This page works exactly the same as mycolleges except posts are sorted by each inidividual college which is determined by which college's url is put in
@app.route("/college/<name>", methods=("GET", "POST"))
def college(name):

    if request.method == "GET":
        college = db_session.query(College).where(College.name == name).first()
        posts = db_session.query(Post).where(Post.post_college == name).order_by(Post.timestamp.desc()).limit(3).all()
        return render_template("collegepage.html", college=college, posts = posts)

    elif request.method == "POST":
        school = request.form["school"]
        body = request.form["body"]
        hash = request.form["hash"]

        
        check = db_session.query(College).where(school == College.name).first()

        if check is not None:
            p = Post(content = body, post_username = session["username"], post_college = school, timestamp = datetime.now())
            db_session.add(p)
            db_session.commit()
            post = db_session.query(Post).where(body == Post.content).first()
            hash = hash.split()
            for tag in hash:
                if db_session.query(Tag).where(tag == Tag.content).first() is None:
                    t = Tag(content = tag)
                    db_session.add(t)
                    db_session.commit()
                tagadded = db_session.query(Tag).where(tag == Tag.content).first()
                new_posttag = PostTag(tag_id = tagadded.id, post_id = post.id)
                db_session.add(new_posttag)
                db_session.commit()
            return redirect(url_for("college", name=name))
        

@app.route("/home")
def home():
    return render_template("home.html")

#Logs out the user by removing the username from the session and returning to the login page
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        flash("You've been logged out", "info")
    return redirect(url_for("login"))


@app.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        #Accepts the various information about the user using the request forms that are found in the corrosponding html page
        uname = request.form["uname"]
        pw = request.form["pw"]
        confirm_pw = request.form["confirm-password"]
        interests = request.form["interests"]
        interests = interests.split()
        check = db_session.query(User).where(User.username == uname).first()
        #Checks to see if username is unique and passwords match before creating a new user entry in the users database
        while True:
            if check == None:
                if pw == confirm_pw:
                    user = User(username = uname, password = pw)
                    db_session.add(user)
                    for college in interests:
                        if(db_session.query(College).where(college == College.name).first() is not None):
                            following = CollegesFollowed(user_username = uname, college_name = college)
                            db_session.add(following)
                        db_session.commit()
                        #logs the user in and sends them to the home page
                session["username"] = uname
                return redirect(url_for("home"))



                        
        




if __name__ == "__main__":
    app.run(debug=True, port=5001)
