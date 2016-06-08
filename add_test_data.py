from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Collection, Category, Link

engine = create_engine('sqlite:///links.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add Collection 1

coll1 = Collection(title="Python",
                   description="Resources for learning Python", path="python")
session.add(coll1)
session.commit()

# Add Collection 1 Categories

coll1cat1 = Category(title="Python Courses",
                     description="Online Python Courses",
                     path="courses",
                     coll_id=1)
session.add(coll1cat1)
session.commit()

coll1cat2 = Category(title="Python Books",
                     description="Online Python Books",
                     path="books",
                     coll_id=1)
session.add(coll1cat2)
session.commit()

coll1cat3 = Category(title="Flask",
                     description="Flask reference, tutorials, and useful links",
                     path="flask",
                     coll_id=1)
session.add(coll1cat3)
session.commit()

# Add Links for Collection 1 Category 1

coll1cat1link1 = Link(title="Udacity: Intro to Computer Science",
                      url="https://www.udacity.com/course/intro-to-computer-science--cs101",
                      description="Learn to build a search engine with this beginner-friendly Python course.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=1)
session.add(coll1cat1link1)
session.commit()

coll1cat1link2 = Link(title="Udacity: Programming Foundations with Python",
                      url="https://www.udacity.com/course/programming-foundations-with-python--ud036",
                      description="Learn Object-Oriented programming with Python. You should know basic programming like if statements, loops, and functions before taking the course. This is a part of Udacity's Full Stack Web Developer Nanodegree.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=1)
session.add(coll1cat1link2)
session.commit()

coll1cat1link4 = Link(title="Coursera: Python for Everybody",
                      url="https://www.coursera.org/specializations/python",
                      description="A series of courses on Coursera created by University of Michigan to teach beginners programming basics in Python and progresses to accessing web data and using databases with Python.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=1)
session.add(coll1cat1link4)
session.commit()

coll1cat1link5 = Link(title="Coursera: An Introduction to Interactive Programming in Python (Part 1)",
                      url="https://www.coursera.org/learn/interactive-python-1",
                      description="Python course on Coursera created by Rice University. Learn Python as you create fun games. If you are a total beginner, you may want to do Python for Everybody first. After you take part 1, you can take part 2 or their entire Fundamentals of Computing Specialization.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=1)
session.add(coll1cat1link5)
session.commit()

coll1cat1link5 = Link(title="Codecademy: Python",
                      url="https://www.codecademy.com/learn/python",
                      description="Learn Python Basics at Codecademy.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=1)
session.add(coll1cat1link5)
session.commit()

# Add Links for Collection 1 Category 2

coll1cat2link1 = Link(title="Python for Kids",
                      url="https://www.nostarch.com/pythonforkids",
                      description="A good Python book (not free) for those new to programming. It says for kids, but it would also be good for adult beginners.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=2)
session.add(coll1cat2link1)
session.commit()

coll1cat2link2 = Link(title="Think Python",
                      url="http://www.greenteapress.com/thinkpython/thinkpython.html",
                      description="Introduction to programming in Python for beginners. You can get an electronic copy for free or you can purchase it.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=2)
session.add(coll1cat2link2)
session.commit()

# Add Links for Collection 1 Category 3

coll1cat3link1 = Link(title="Flask Mega-Tutorial",
                      url="http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
                      description="An 18-part Flask tutorial by Miguel Grinberg",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=3)
session.add(coll1cat3link1)
session.commit()

coll1cat3link1 = Link(title="Python Web Applications with Flask",
                      url="https://realpython.com/blog/python/python-web-applications-with-flask-part-i/",
                      description="A 3-part Flask tutorial on the Real Python blog. If you click on the courses link on the realpython.com page, course 2 is about Flask as well, but it is not free.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=3)
session.add(coll1cat3link1)
session.commit()

# Add Collection 2

coll2 = Collection(title="JavaScript",
                   description="Resources for learning JavaScript",
                   path="javascript")
session.add(coll2)
session.commit()

# Add Collection Categories

coll2cat4 = Category(title="JavaScript Courses",
                     description="Online JavaScript Courses",
                     path="courses",
                     coll_id=2)
session.add(coll2cat4)
session.commit()

coll2cat5 = Category(title="JavaScript Books",
                     description="Online JavaScript Books",
                     path="books",
                     coll_id=2)
session.add(coll2cat5)
session.commit()

coll2cat6 = Category(title="JQuery",
                     description="jQuery Links",
                     path="jquery",
                     coll_id=2)
session.add(coll2cat6)
session.commit()

# Add Links for Collection 2 Category 4

coll2cat4link1 = Link(title="Udacity: JavaScript Basics",
                      url="https://www.udacity.com/course/javascript-basics--ud804",
                      description="This Udacity course teaches you the basics of JavaScript. The course is a part of Udacity's Front-End Web Developer Nanodegree, but can also be taken for free.",
                      submitter="example@example.com",
                      coll_id=2,
                      cat_id=4)
session.add(coll2cat4link1)
session.commit()

coll2cat4link1 = Link(title="Codecademy: JavaScript",
                      url="https://www.codecademy.com/learn/javascript",
                      description="Learn JavaScript basics from Codecademy.",
                      submitter="example@example.com",
                      coll_id=2,
                      cat_id=4)
session.add(coll2cat4link1)
session.commit()

# Add Links for Collection 2 Category 5

coll2cat5link1 = Link(title="Head First JavaScript Programming",
                      url="http://shop.oreilly.com/product/0636920027065.do",
                      description="A great JavaScript programming book (not free) that has clear explanations of object-oriented programming and closures, perhaps best for those with a little JavaScript knowledge already.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=5)
session.add(coll2cat5link1)
session.commit()

coll2cat5link2 = Link(title="JavaScript for Kids",
                      url="https://www.nostarch.com/jsforkids",
                      description="A good JavaScript book (not free) for those new to programming. It says for kids, but it would also be good for adult beginners.",
                      submitter="example@example.com",
                      coll_id=1,
                      cat_id=5)
session.add(coll2cat5link2)
session.commit()

coll2cat5link3 = Link(title="You don't know JS series",
                      url="https://github.com/getify/You-Dont-Know-JS",
                      description="These 6 books are not for beginners, and will help you go deeper into some JavaScript topics. The ebook versions are free.",
                      submitter="example@example.com",
                      coll_id=2,
                      cat_id=5)
session.add(coll2cat5link3)
session.commit()

# Add Links for Collection 2 Category 6

coll2cat6link1 = Link(title="Udacity: Intro to jQuery",
                      url="https://www.udacity.com/course/intro-to-jquery--ud245",
                      description="Learn jQuery basics from Udacity.",
                      submitter="example@example.com",
                      coll_id=2,
                      cat_id=6)
session.add(coll2cat6link1)
session.commit()

coll2cat6link2 = Link(title="edX: Introduction to jQuery",
                      url="https://www.edx.org/course/introduction-jquery-microsoft-dev208x-1",
                      description="jQuery tutorial by Microsoft on edX.",
                      submitter="example@example.com",
                      coll_id=2,
                      cat_id=6)
session.add(coll2cat6link2)
session.commit()

# Add Collection 3

coll3 = Collection(title="HTML and CSS",
                   description="Resources for learning HTML and CSS",
                   path="htmlcss")
session.add(coll3)
session.commit()

# Add Collection 3 Categories

coll3cat1 = Category(title="HTML and CSS Courses",
                     description="Online HTML and CSS Courses",
                     path="courses",
                     coll_id=3)
session.add(coll3cat1)
session.commit()

coll3cat2 = Category(title="HTML and CSS Books",
                     description="Online HTML and CSS Books",
                     path="books",
                     coll_id=3)
session.add(coll3cat2)
session.commit()

coll3cat2 = Category(title="HTML and CSS Reference",
                     description="HTML and CSS Reference",
                     path="reference",
                     coll_id=3)
session.add(coll3cat2)
session.commit()

# Add Links for Collection 3 Category 7

coll3cat7link1 = Link(title="Codecademy: HTML & CSS",
                      url="https://www.codecademy.com/learn/web",
                      description="A good place for beginners to get started learning HTML and CSS",
                      submitter="example@example.com",
                      coll_id=3,
                      cat_id=7)
session.add(coll3cat7link1)
session.commit()

coll3cat7link2 = Link(title="Udacity: Intro to HTML & CSS",
                      url="https://www.udacity.com/course/intro-to-html-and-css--ud304",
                      description="Learn not only HTML and CSS, but also how to turn a design mockup into a webpage, as well as some responsive design techniques.",
                      submitter="example@example.com",
                      coll_id=3,
                      cat_id=7)
session.add(coll3cat7link2)
session.commit()

# Add Links for Collection 3 Category 8

coll3cat8link1 = Link(title="Head First HTML with CSS & XHTML",
                      url="https://www.udacity.com/course/intro-to-html-and-css--ud304",
                      description="A good book for those starting out with HTML and CSS.",
                      submitter="example@example.com",
                      coll_id=3,
                      cat_id=8)
session.add(coll3cat8link1)
session.commit()

# Add Links for Collection 3 Category 9

coll3cat9link1 = Link(title="MDN: HTML",
                      url="https://developer.mozilla.org/en-US/docs/Web/HTML",
                      description="HTML reference, guides, and tutorials",
                      submitter="example@example.com",
                      coll_id=3,
                      cat_id=9)
session.add(coll3cat9link1)
session.commit()

coll3cat9link2 = Link(title="MDN: CSS",
                      url="https://developer.mozilla.org/en-US/docs/Web/CSS",
                      description="CSS reference, tutorials, and demos",
                      submitter="example@example.com",
                      coll_id=3,
                      cat_id=9)
session.add(coll3cat9link2)
session.commit()

print("Added items to the database!")