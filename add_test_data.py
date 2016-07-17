from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Users, Base, Collection, Category, Link

engine = create_engine('postgresql:///links')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# add dummy user
User1 = Users(provider="test", name="A. Test", email="test@example.com", is_admin=False)
session.add(User1)
session.commit()

# Add Collection 1

coll1 = Collection(name="Python",
                   description="Resources for learning Python",
                   path="python",
                   user_id=1)
session.add(coll1)
session.commit()

# Add Collection 1 Categories

coll1cat1 = Category(name="Python Courses",
                     description="Online Python Courses",
                     path="courses",
                     coll_id=1,
                     user_id=1)
session.add(coll1cat1)
session.commit()

coll1cat2 = Category(name="Python Books",
                     description="Online Python Books",
                     path="books",
                     coll_id=1,
                     user_id=1)
session.add(coll1cat2)
session.commit()

coll1cat3 = Category(name="Flask",
                     description="Flask reference, tutorials, and useful links",
                     path="flask",
                     coll_id=1,
                     user_id=1)
session.add(coll1cat3)
session.commit()

# Add Links for Collection 1 Category 1

coll1cat1link1 = Link(name="Udacity: Intro to Computer Science",
                      url="https://www.udacity.com/course/intro-to-computer-science--cs101",
                      description="Learn to build a search engine with this beginner-friendly Python course.",
                      coll_id=1,
                      cat_id=1,
                      user_id=1)
session.add(coll1cat1link1)
session.commit()

coll1cat1link2 = Link(name="Udacity: Programming Foundations with Python",
                      url="https://www.udacity.com/course/programming-foundations-with-python--ud036",
                      description="Learn Object-Oriented programming with Python. You should know basic programming like if statements, loops, and functions before taking the course. This is a part of Udacity's Full Stack Web Developer Nanodegree.",
                      coll_id=1,
                      cat_id=1,
                      user_id=1)
session.add(coll1cat1link2)
session.commit()

coll1cat1link4 = Link(name="Coursera: Python for Everybody",
                      url="https://www.coursera.org/specializations/python",
                      description="A series of courses on Coursera created by University of Michigan to teach beginners programming basics in Python and progresses to accessing web data and using databases with Python.",
                      coll_id=1,
                      cat_id=1,
                      user_id=1)
session.add(coll1cat1link4)
session.commit()

coll1cat1link5 = Link(name="Coursera: An Introduction to Interactive Programming in Python (Part 1)",
                      url="https://www.coursera.org/learn/interactive-python-1",
                      description="Python course on Coursera created by Rice University. Learn Python as you create fun games. If you are a total beginner, you may want to do Python for Everybody first. After you take part 1, you can take part 2 or their entire Fundamentals of Computing Specialization.",
                      coll_id=1,
                      cat_id=1,
                      user_id=1)
session.add(coll1cat1link5)
session.commit()

coll1cat1link5 = Link(name="Codecademy: Python",
                      url="https://www.codecademy.com/learn/python",
                      description="Learn Python Basics at Codecademy.",
                      coll_id=1,
                      cat_id=1,
                      user_id=1)
session.add(coll1cat1link5)
session.commit()

# Add Links for Collection 1 Category 2

coll1cat2link1 = Link(name="Python for Kids",
                      url="https://www.nostarch.com/pythonforkids",
                      description="A good Python book (not free) for those new to programming. It says for kids, but it would also be good for adult beginners.",
                      coll_id=1,
                      cat_id=2,
                      user_id=1)
session.add(coll1cat2link1)
session.commit()

coll1cat2link2 = Link(name="Think Python",
                      url="http://www.greenteapress.com/thinkpython/thinkpython.html",
                      description="Introduction to programming in Python for beginners. You can get an electronic copy for free or you can purchase it.",
                      coll_id=1,
                      cat_id=2,
                      user_id=1)
session.add(coll1cat2link2)
session.commit()

# Add Links for Collection 1 Category 3

coll1cat3link1 = Link(name="Flask Mega-Tutorial",
                      url="http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
                      description="An 18-part Flask tutorial by Miguel Grinberg",
                      coll_id=1,
                      cat_id=3,
                      user_id=1)
session.add(coll1cat3link1)
session.commit()

coll1cat3link1 = Link(name="Python Web Applications with Flask",
                      url="https://realpython.com/blog/python/python-web-applications-with-flask-part-i/",
                      description="A 3-part Flask tutorial on the Real Python blog. If you click on the courses link on the realpython.com page, course 2 is about Flask as well, but it is not free.",
                      coll_id=1,
                      cat_id=3,
                      user_id=1)
session.add(coll1cat3link1)
session.commit()

# Add Collection 2

coll2 = Collection(name="JavaScript",
                   description="Resources for learning JavaScript",
                   path="javascript",
                   user_id=1)
session.add(coll2)
session.commit()

# Add Collection Categories

coll2cat4 = Category(name="JavaScript Courses",
                     description="Online JavaScript Courses",
                     path="courses",
                     coll_id=2,
                     user_id=1)
session.add(coll2cat4)
session.commit()

coll2cat5 = Category(name="JavaScript Books",
                     description="Online JavaScript Books",
                     path="books",
                     coll_id=2,
                     user_id=1)
session.add(coll2cat5)
session.commit()

coll2cat6 = Category(name="JQuery",
                     description="jQuery Links",
                     path="jquery",
                     coll_id=2,
                     user_id=1)
session.add(coll2cat6)
session.commit()

# Add Links for Collection 2 Category 4

coll2cat4link1 = Link(name="Udacity: JavaScript Basics",
                      url="https://www.udacity.com/course/javascript-basics--ud804",
                      description="This Udacity course teaches you the basics of JavaScript. The course is a part of Udacity's Front-End Web Developer Nanodegree, but can also be taken for free.",
                      coll_id=2,
                      cat_id=4,
                      user_id=1)
session.add(coll2cat4link1)
session.commit()

coll2cat4link1 = Link(name="Codecademy: JavaScript",
                      url="https://www.codecademy.com/learn/javascript",
                      description="Learn JavaScript basics from Codecademy.",
                      coll_id=2,
                      cat_id=4,
                      user_id=1)
session.add(coll2cat4link1)
session.commit()

# Add Links for Collection 2 Category 5

coll2cat5link1 = Link(name="Head First JavaScript Programming",
                      url="http://shop.oreilly.com/product/0636920027065.do",
                      description="A great JavaScript programming book (not free) that has clear explanations of object-oriented programming and closures, perhaps best for those with a little JavaScript knowledge already.",
                      coll_id=1,
                      cat_id=5,
                      user_id=1)
session.add(coll2cat5link1)
session.commit()

coll2cat5link2 = Link(name="JavaScript for Kids",
                      url="https://www.nostarch.com/jsforkids",
                      description="A good JavaScript book (not free) for those new to programming. It says for kids, but it would also be good for adult beginners.",
                      coll_id=1,
                      cat_id=5,
                      user_id=1)
session.add(coll2cat5link2)
session.commit()

coll2cat5link3 = Link(name="You don't know JS series",
                      url="https://github.com/getify/You-Dont-Know-JS",
                      description="These 6 books are not for beginners, and will help you go deeper into some JavaScript topics. The ebook versions are free.",
                      coll_id=2,
                      cat_id=5,
                      user_id=1)
session.add(coll2cat5link3)
session.commit()

# Add Links for Collection 2 Category 6

coll2cat6link1 = Link(name="Udacity: Intro to jQuery",
                      url="https://www.udacity.com/course/intro-to-jquery--ud245",
                      description="Learn jQuery basics from Udacity.",
                      coll_id=2,
                      cat_id=6,
                      user_id=1)
session.add(coll2cat6link1)
session.commit()

coll2cat6link2 = Link(name="edX: Introduction to jQuery",
                      url="https://www.edx.org/course/introduction-jquery-microsoft-dev208x-1",
                      description="jQuery tutorial by Microsoft on edX.",
                      coll_id=2,
                      cat_id=6,
                      user_id=1)
session.add(coll2cat6link2)
session.commit()

# Add Collection 3

coll3 = Collection(name="HTML and CSS",
                   description="Resources for learning HTML and CSS",
                   path="htmlcss",
                   user_id=1)
session.add(coll3)
session.commit()

# Add Collection 3 Categories

coll3cat1 = Category(name="HTML and CSS Courses",
                     description="Online HTML and CSS Courses",
                     path="courses",
                     coll_id=3,
                     user_id=1)
session.add(coll3cat1)
session.commit()

coll3cat2 = Category(name="HTML and CSS Books",
                     description="Online HTML and CSS Books",
                     path="books",
                     coll_id=3,
                     user_id=1)
session.add(coll3cat2)
session.commit()

coll3cat2 = Category(name="HTML and CSS Reference",
                     description="HTML and CSS Reference",
                     path="reference",
                     coll_id=3,
                     user_id=1)
session.add(coll3cat2)
session.commit()

# Add Links for Collection 3 Category 7

coll3cat7link1 = Link(name="Codecademy: HTML & CSS",
                      url="https://www.codecademy.com/learn/web",
                      description="A good place for beginners to get started learning HTML and CSS",
                      coll_id=3,
                      cat_id=7,
                      user_id=1)
session.add(coll3cat7link1)
session.commit()

coll3cat7link2 = Link(name="Udacity: Intro to HTML & CSS",
                      url="https://www.udacity.com/course/intro-to-html-and-css--ud304",
                      description="Learn not only HTML and CSS, but also how to turn a design mockup into a webpage, as well as some responsive design techniques.",
                      coll_id=3,
                      cat_id=7,
                      user_id=1)
session.add(coll3cat7link2)
session.commit()

# Add Links for Collection 3 Category 8

coll3cat8link1 = Link(name="Head First HTML with CSS & XHTML",
                      url="https://www.udacity.com/course/intro-to-html-and-css--ud304",
                      description="A good book for those starting out with HTML and CSS.",
                      coll_id=3,
                      cat_id=8,
                      user_id=1)
session.add(coll3cat8link1)
session.commit()

# Add Links for Collection 3 Category 9

coll3cat9link1 = Link(name="MDN: HTML",
                      url="https://developer.mozilla.org/en-US/docs/Web/HTML",
                      description="HTML reference, guides, and tutorials",
                      coll_id=3,
                      cat_id=9,
                      user_id=1)
session.add(coll3cat9link1)
session.commit()

coll3cat9link2 = Link(name="MDN: CSS",
                      url="https://developer.mozilla.org/en-US/docs/Web/CSS",
                      description="CSS reference, tutorials, and demos",
                      coll_id=3,
                      cat_id=9,
                      user_id=1)
session.add(coll3cat9link2)
session.commit()

print("Added items to the database!")