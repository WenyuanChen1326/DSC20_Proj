"""
DSC 20 Final Project
Name: Wenyuan Chen
PID: A15516589
"""
from util import Stack, Queue
from datetime import datetime


def doctest():
    """
    ------------------------ PRODUCT TEST ------------------------

    >>> p1 = Product("iphone",399)
    >>> p2 = Special_Product("macbook air",999)
    >>> p3 = Limited_Product("free iphone", 0, 10)
    >>> p1, p2, p3
    (PRODUCT <0>, PRODUCT <1>, PRODUCT <2>)
    >>> print(p1)
    <0> iphone - 399$
    >>> print(p2)
    <1> macbook air - 999$ (special)
    >>> print(p3)
    <2> free iphone - 0$ (10 left)

    ------------------------ WAREHOUSE TEST ------------------------

    >>> wh = Warehouse()
    >>> st = Store(wh)
    >>> wh.import_product(p1)
    >>> wh.import_product(p2)
    >>> wh.import_product(p3)
    >>> print(wh)
    Warehouse with 3 products
    >>> print(wh.get_product(1))
    <1> macbook air - 999$ (special)
    >>> st.view_products()
    ============================
    <ID> Product - Price
    <0> iphone - 399$
    <1> macbook air - 999$ (special)
    <2> free iphone - 0$ (10 left)
    ============================
    >>> wh.export_product(3)
    >>> wh.export_product(2)
    PRODUCT <2>
    >>> wh.remove_product(0)
    True
    >>> st.view_products()
    ============================
    <ID> Product - Price
    <1> macbook air - 999$ (special)
    <2> free iphone - 0$ (9 left)
    ============================
    >>> st.view_products(sort = True)
    ============================
    <ID> Product - Price
    <2> free iphone - 0$ (9 left)
    <1> macbook air - 999$ (special)
    ============================
    >>> wh.remove_product(0)
    False
    >>> [wh.export_product(2) for i in range(9)]
    [PRODUCT <2>, PRODUCT <2>, PRODUCT <2>, PRODUCT <2>, PRODUCT <2>,\
 PRODUCT <2>, PRODUCT <2>, PRODUCT <2>, PRODUCT <2>]
    >>> st.view_products()
    ============================
    <ID> Product - Price
    <1> macbook air - 999$ (special)
    ============================
    
    >>> print(p3)
    <2> free iphone - 0$ (0 left)
   
    >>> wh.show_log()
    Product <0> imported - 2020-11-26 07:09:17.709522
    Product <1> imported - 2020-11-26 07:09:17.709584
    Product <2> imported - 2020-11-26 07:09:17.709612
    Product <2> exported - 2020-11-26 07:09:17.709745
    Product <0> removed  - 2020-11-26 07:09:17.709776
    Product <2> exported - 2020-11-26 07:09:17.709886
    Product <2> exported - 2020-11-26 07:09:17.709893
    Product <2> exported - 2020-11-26 07:09:17.709897
    Product <2> exported - 2020-11-26 07:09:17.709901
    Product <2> exported - 2020-11-26 07:09:17.709905
    Product <2> exported - 2020-11-26 07:09:17.709909
    Product <2> exported - 2020-11-26 07:09:17.709913
    Product <2> exported - 2020-11-26 07:09:17.709916
    Product <2> exported - 2020-11-26 07:09:17.709920
    Product <2> removed  - 2020-11-26 07:09:17.709924

    ------------------------ USER TEST ------------------------

    >>> u1 = User( 'Jerry', st)
    >>> u2 = Premium_User( 'FYX', st)
    >>> u1
    USER<0>
    >>> u2
    USER<1>
    >>> print(u1)
    standard user: Jerry - 0$
    >>> u2.add_balance(2000)
    >>> print(u2)
    premium user: FYX - 2000$
    
    >>> wh.import_product(p1)
    >>> u1 = User("A",st)
    >>> u1.add_cart(0)
    >>> u1.add_cart(0)
    >>> u1.view_cart()
    (front) <0> iphone - 399$ -- <0> iphone - 399$ (rear)
    >>> u1.checkout()
    STORE: Not enough money QQ
    []
    >>> u1.add_balance(1000)
    >>> u1.checkout()
    STORE: A ordered iphone. A has 562$ left.
    STORE: A ordered iphone. A has 124$ left.
    [PRODUCT <0>, PRODUCT <0>]
    >>> p4 = Limited_Product("Ipad", 600, 5)
    >>> wh.import_product(p4)
    >>> u2.buy_all(3)
    STORE: FYX ordered Ipad. FYX has 1400$ left.
    STORE: FYX ordered Ipad. FYX has 800$ left.
    STORE: FYX ordered Ipad. FYX has 200$ left.
    STORE: Not enough money QQ
    [PRODUCT <3>, PRODUCT <3>, PRODUCT <3>]

    ------------------- HISTORY / UNDO TEST -------------------

    >>> u1.view_history()
    (bottom) <0> 2 bought <0> iphone - 399$ at 2020-12-03 21:27:54.903632 -- \
<1> 2 bought <0> iphone - 399$ at 2020-12-03 21:27:54.903658 (top)
    >>> u1.undo_purchase()
    STORE: A refunded iphone. A has 523$ left.

    -------------------------- EC TEST ------------------------
    >>> p1 = Product("A",20)
    >>> p2 = Special_Product("B",7)
    >>> p3 = Limited_Product("C", 1, 2)
    >>> wh = Warehouse()
    >>> wh.import_product(p1)
    >>> wh.import_product(p2)
    >>> wh.import_product(p3)
    >>> st = Store(wh)
    >>> st.view_products()
    ============================
    <ID> Product - Price
    <4> A - 20$
    <5> B - 7$ (special)
    <6> C - 1$ (2 left)
    ============================
    >>> st.so_rich(45)
    1
    >>> st.so_rich(61)
    0
    >>> st.so_rich_recursive(45)
    1
    >>> st.so_rich_recursive(61)
    0
    >>> st.so_rich_recursive(90)
    0
    >>> st.so_rich_recursive(101)
    0
    >>> [print(st.so_rich(i), st.so_rich_recursive(i)) for i in range(200) if st.so_rich(i) != st.so_rich_recursive(i)]
    []
    """
    pass


#######################################################################
#                               PRODUCT                               #
#######################################################################
class Product:
    """ 
    A class named Product creates product instances, each of which representing
    a kind of products.
    """
    product_counter = 0
    ##### Part 1.1 #####
    def __init__(self, name, price):
        """ 
        A constructor that creates product instance with 3 instance attributes
        """
        self.name = name
        self.price = price
        self.id = self.product_counter
        Product.product_counter += 1

    def __str__(self):
        """ A string representation with the following format"""
        return "<{0}> {1} - {2}$".format(self.id, self.name, self.price)

    def __repr__(self):
        """ A repr representation with the following format"""
        return "PRODUCT <{}>".format(self.id)


class Limited_Product(Product):
    """ 
    A subclass of Class product that creates limited product instances.
    """

    ##### Part 1.2 #####
    def __init__(self, name, price, amount):
        """
        A constructor that creats limited product instance with the following
        instance attributes
        """
        # YOUR CODE GOES HERE #
        super().__init__(name, price)
        self.amount = amount

    def __str__(self):
        """ 
        A string representation of class Limited_Product with the following
        format
        """
        return "<{0}> {1} - {2}$ ({3} left)".format(self.id, self.name, \
            self.price, self.amount)


class Special_Product(Product):
    """
    A subclass named Special_Products of clss product that creats speicial 
    product instance for premium users only
    """

    ##### Part 1.3 #####
    def __init__(self, name, price, description="special"):
        """ 
        A constructor that creates the special product instance with the
        following instance attributes
        """
        super().__init__(name, price)
        self.description = description

    def __str__(self):
        """ 
        A string representation of class Special_Product with the following
        format
        """
        return "<{0}> {1} - {2}$ ({3})".format(self.id, self.name, \
            self.price, self.description)


#######################################################################
#                              WAREHOUSE                              #
#######################################################################


class Warehouse:
    """ 
    A class named Warehouse that creats warehouse instances, which stores
    all products for a particular store.
    """

    ##### Part 2 #####
    def __init__(self):
        """
        A constructor that creates the warehouse instance with 2 instance 
        attributes
        """
        self.inventory = {}
        self.log = []

    def __str__(self):
        """
        A string representation of class Warehouse with the following
        format
        """
        return "Warehouse with {} products".format(len(self.inventory.keys()))


    def get_product(self, product_id):
        """
        A getter method to get the product instance with its given id from the 
        inverntory
        """
        if product_id not in self.inventory:
            return None
        return self.inventory[product_id]

    def list_products(self):
        """
        A method that returns a list of all actual product instance stored 
        in the inventory
        """
        return list(self.inventory.values())

    def remove_product(self, product_id):
        """
        A method that removes the product in the inventory dict. Return True
        if successfully done. Return False otherwise. Update the log.
        """
        if product_id not in self.inventory:
            return False
        else:
            del self.inventory[product_id]
            time_log = str(datetime.now())
            self.log.append("Product <{0}> removed  - {1}".format(product_id,\
            time_log))
            return True
    def import_product(self, product):
        """
        A method that appends a new product instance to the inventory and
        update log
        """
        if product.id not in self.inventory:
            self.inventory[product.id] = product
            time_log = str(datetime.now())
            self.log.append("Product <{0}> imported - {1}".format(product.id,\
            time_log))

    def export_product(self, product_id):
        """
        A method that export the product instance with the given id (int) 
        from the inventory.
        """
        if product_id not in self.inventory:
            return None
        product_instance = self.inventory[product_id]
        time_log = str(datetime.now())
        self.log.append("Product <{0}> exported - {1}".format(product_id, \
            time_log))
        if type(self.inventory[product_id]) == Limited_Product:
            product_instance.amount -= 1
            if product_instance.amount == 0:
                self.remove_product(product_id)
        return product_instance
        
    def size(self):
        """
        A funciton that returns the number of products stored in the inventory
        """
        return len(self.inventory.keys())
    def show_log(self):
        """
        Print all log strings in the log
        """
        for log in self.log:
            print(log)
            
#######################################################################
#                               HISTORY                               #
#######################################################################
class History:
    """
    A class History that provides abstraction to the purchase history records.
    """
    history_counter = 0
    ##### Part 3 #####
    def __init__(self, product, user):
        """
        A constructor that creats a history instance for a store to record
        """
        self.product = product
        self.user = user
        self.id = self.history_counter
        self.time = datetime.now()
        History.history_counter += 1

    def __str__(self):
        """
        A string representation with the following format
        """
        return "<{0}> {1} bought {2} at {3}".format(self.id, self.user.id,\
            self.product, self.time)

    def __repr__(self):
        """
        A string representation with the following format
        """
        return "HISTORY<{0}> - {1}".format(self.id, self.time)


#######################################################################
#                                USER                                 #
#######################################################################
class User:
    """
    The class User provides abstraction to the user instance
    """
    user_counter = 0
    ##### Part 4.1 #####
    def __init__(self, name, store):
        """
        A constructor that creates user instance with the following attributes
        """
        self.name = name
        self.store = store
        self.balance = 0
        self.id = self.user_counter
        self.purchase_history = Stack()
        self.cart = Queue()
        User.user_counter += 1
        self.store.add_user(self)

    def __str__(self):
        """
        Return the string representation with the following format
        """
        return "standard user: {0} - {1}$".format(self.name, self.balance)

    def __repr__(self):
        """
        Return repr representation with the followin format
        """
        return "USER<{}>".format(self.id)

    def set_name(self, new_name):
        """
        A method that sets the name attribute to the new_name
        """
        self.name = new_name

    def get_name(self):
        """
        A getter method that gets the name attribute
        """
        return self.name

    def set_balance(self, amount):
        """
        A setter method that sets the balance to the amount
        """
        self.balance = amount

    def get_balance(self):
        """ 
        A getter method that gets the balance
        """
        return self.balance

    def add_balance(self, amount):
        """
        A method that adds amount to the self.amount
        """
        self.balance += amount

    def last_purchase(self):
        """
        A method that retrieves and return the last purchased history instance
        """
        return self.purchase_history.peek()

    def view_history(self):
        """
        Print the purchase history of this user
        """
        print(self.purchase_history)

    def view_cart(self):
        """
        Print the cart of this user
        """
        print(self.cart)

    def clear_cart(self):
        """
        Remove all prodcuts in the cart
        """
        self.cart.clear()

    ##### Part 5.2 #####
    def add_cart(self, product_id):
        """
        A function that takes a product id and adds the corresponding product
        to the shopping cart.
        """
        inventory = self.store.warehouse.inventory
        if product_id in inventory:
            self.cart.enqueue(inventory[product_id])

    def checkout(self):
        """
        A functin that orders every item in the shopping cart and return a
        list of purchased products
        """
        lst_purchased_products = []

        for product in self.cart.items:
            order = self.store.order(self.id, product.id)
            if order:
                self.cart.dequeue()
                lst_purchased_products.append(product)
                self.purchase_history.push(order)
            else:
                break
        return lst_purchased_products

    ##### Part 5.3 #####
    def undo_purchase(self):
        """
        A function that undoes the last purchase of the user.
        """
        if self.purchase_history.is_empty():
            print("USER: no purchase history")
            return
        last_purchase_instance = self.last_purchase().product
        if self.store.undo_order(self.id, last_purchase_instance):
            self.purchase_history.pop()
 

class Premium_User(User):
    """ 
    A subclass of Class User that provides abstraction to the premium users
    instance.
    """
    ##### Part 4.2 #####
    def __str__(self):
        """
        A string representation with the following format
        """
        return "premium user: {0} - {1}$".format(self.name, self.balance)

    ##### Part 5.4 #####
    def buy_all(self, product_id):
        """
        A function that supports batch ordering for limited products. 
        It takes product it as parameter
        """
        lst_purchased_products =[]
        product_ins = self.store.get_product(product_id)
        if type(product_ins) != Limited_Product:
            print("USER: not a limited product")
            return lst_purchased_products
        while product_ins.amount >= 0:
            order = self.store.order(self.id, product_id)
            if order:
                lst_purchased_products.append(product_ins)
                self.purchase_history.push(order)
            else:
                break
        return lst_purchased_products

    def undo_all(self):
        """
        A function that iteratively cancels the last purchases until the user 
        does not have any records in purchase history, or the last purchase 
        is a limited product.
        """
        while not self.purchase_history.is_empty() and not \
        type(self.last_purchase().product) == Limited_Product:
            self.undo_purchase()


#######################################################################
#                               STORE                                 #
#######################################################################
class Store:
    """
    A class Store provides abstrction to the stores
    """
    ##### Part 4.3 #####
    def __init__(self, warehouse):
        """
        A constructor for the store instance with the following attributes
        """
        self.users = {}
        self.warehouse = warehouse

    def __str__(self):
        """
        A string representation with the following format
        """
        return "STORE: store with {0} users and {1} products".format(\
            len(self.users), self.warehouse.size())

    def get_product(self, product_id):
        """ 
        A getter method that get a product instance with the provided id 
        """
        return self.warehouse.get_product(product_id)

    def view_products(self, sort=False):
        """
        Print all products in the inventory with either ascending or descending
        order
        """
        if not sort:
            print("============================")
            print("<ID> Product - Price")
            normal_inventory = self.warehouse.inventory
            for i in normal_inventory:
                print(normal_inventory[i])
            print("============================")
        else:
            print("============================")
            print("<ID> Product - Price")
            sorted_inventory = dict(sorted(self.warehouse.inventory.items(), \
                key=lambda product:product[1].price))
            for i in sorted_inventory:
                print(sorted_inventory[i])
            print("============================")
    ##### Part 5.1 #####
    def add_user(self, user):
        """
        A function that takes a user instance and add this user to the
        self.user dictionary if not existed already
        """
        if user in self.users.values():
            print("STORE: User already exists")
            return False
        else:
            self.users[user.id] = user
            return True

    ##### Part 5.2 #####
    def order(self, user_id, product_id):
        """
        A function that takes the ids of the user who makes the order of the
        products
        """
        shipping_factor = 1.1
        inventory = self.warehouse.inventory
        product = self.get_product(product_id)
        user = self.users[user_id]
        if product_id not in inventory:
            print("STORE: Product not found")
            return False
        if type(user) != Premium_User and\
        type(inventory[product_id]) == Special_Product:
            print ("STORE: Special product is limited to premium user")
            return False
        if type(user) == Premium_User:
            if user.balance < inventory[product_id].price:
                print("STORE: Not enough money QQ")
                return False
            user.balance -= inventory[product_id].price
        else:
            total_price = int(shipping_factor * inventory[product_id].price)
            if \
            user.balance < total_price:
                print("STORE: Not enough money QQ")
                return False
            user.balance -= total_price
        self.warehouse.export_product(product_id)
        print("STORE: {0} ordered {1}. {2} has {3}$ left.".\
            format(user.name,  product.name,\
                user.name, user.balance))
        return History(product, user)


    ##### Part 5.3 #####
    def undo_order(self, user_id, product):
        """
        A function that takes the usder id and the product instance undos 
        the order
        """
        if type(product) == Limited_Product:
            print("STORE: can't refund Limited_Product")
            return False
        user_ins = self.users[user_id]
        user_ins.balance += product.price
        print("STORE: {0} refunded {1}. {2} has {3}$ left.".\
        format(user_ins.name, product.name, user_ins.name, user_ins.balance))
        return True

    ##### Part 6 #####
    def so_rich(self, money):
        """
        A function that finds out the a sequence of purchase that yields the
        least amount of left-over moeny and returns the amount.
        """

        # suppose you haven't seen any product yet
        # the only possible amount of money left is "money"
        # this is a set to record the possible money left
        left = set([money])

        # get products
        lst = self.warehouse.list_products()

        for product in lst:

            # a temporary set to save the updates of "left"
            # you don't want to modify the set you're iterating through
            tmp_left = set()

            for m in left:
                # update tmp_left
                if type(product) != Limited_Product:
                    new_left = m
                    while new_left >= 0:
                        tmp_left.add(new_left)
                        new_left = new_left - product.price
                else:
                    # handle limited product
                    new_left = m
                    amount = product.amount
                    while new_left >= 0 and amount >= 0:
                        tmp_left.add(new_left)
                        new_left -= product.price
                        amount -= 1
            left = left.union(tmp_left)

        return min(left)

    def so_rich_recursive(self, money):
        """
        A recursion method that finds out the a sequence of purchase that 
        yields the least amount of left-over moeny and returns the amount.
        """

        # get products
        lst = self.warehouse.list_products()

        def helper(lst, money):
            # base case
            if money == 0:
                return 0
            if len(lst) == 0:
                return money
            cur_min = money
            product = lst[0]
            if type(product) != Limited_Product:
                tmp = money
                while tmp >= 0:
                    skip_first = helper(lst[1:], tmp)
                    cur_min = min(skip_first, cur_min)
                    tmp -= product.price
            else:
                tmp = money
                amount = product.amount
                while tmp >= 0 and amount >= 0:
                    skip_first = helper(lst[1:], tmp)
                    tmp -= product.price
                    amount -= 1
                    cur_min = min(skip_first, cur_min)
            return cur_min

        return helper(lst, money)
