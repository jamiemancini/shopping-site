"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True



@app.route("/")
def index():
    """Return homepage."""
    session['visited_homepage']=True

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    #the route melons does a get_all on melons
    #if you look at the top, you will see melons is being imported
    #with the code 'import melon'
    #if you look at the file melons.py you will see the class melons
    #its attributes and methods
    #the get_all() method returns a list of melon instances and their attibutes
    #melon_list is a list of instances of the melon class

    #the melon-list is being passed into "all_melons.html" with the command below

    #example of showing session that was initiated on homepage
    #we used .get, because if you access the homepage and the sessions is
    #empty you will get an error
    #this is the way around it
    print(session.get('visited_homepage', False))
    
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>") #a variable route 
#whatever comes after the slash so here '<melon_id>'
#it is passed on to the next line
def show_melon(melon_id): #melon_id comes from the URL
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""
     
     # - get the cart dictionary from the session
    cart = session.get('cart',{})
    
    # - create a list to hold melon objects and a variable to hold the total
    melons_in_cart=[]
    order_cost=0
    
    # - loop over the cart dictionary, and for each melon id:
    for melon_id, order_count in cart.items():
        
        # - get the corresponding Melon object
        current_melon=melons.get_by_id(melon_id)
        
        #- compute the total cost for that type of melon
        current_melon.current_total_cost=current_melon.price*order_count
        # - add quantity and total cost as attributes on the Melon object
        current_melon.quantity = order_count

         #  - add this to the order total
        order_cost += current_melon.current_total_cost

         #    - add the Melon object to the list created above
        melons_in_cart.append(current_melon)

   
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

     # - pass the total order cost and the list of Melon objects to the template
    return render_template("cart.html", melons_in_cart=melons_in_cart, total_order_cost=order_cost)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""


    # session['cart' {melon_id: # of times it was added}]
    if 'cart' not in session:
        session['cart']={}
    current_cart=session['cart']
    if melon_id not in current_cart:
        current_cart[melon_id]=0
    current_cart[melon_id] += 1
    
    session["cart"]=current_cart
    flash("Melon successfully added to cart!")
    return redirect('/cart')
   


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    
    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
