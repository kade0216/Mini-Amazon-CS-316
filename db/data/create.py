import random, string, csv
db = 'db/data/'

def createUser():
    fnames= ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle']

    lnames= ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green']

    streets= ['Second', 'Third', 'First', 'Fourth', 'Park', 'Fifth', 'Main', 'Sixth', 'Oak', 'Seventh', 'Pine', 'Maple', 'Cedar', 'Eighth', 'Elm', 'View', 'Washington', 'Ninth', 'Lake', 'Hill']

    with open(db + 'Users.csv', mode='w') as f:
        for i in range(500):
            id = i
            fname = random.choice(fnames)
            lname = random.choice(lnames)
            address = str(random.randint(1, 1000)) + ' ' + random.choice(streets) + ' St.'
            balance = random.randint(0,100000)
            email = fname[0]+lname+str(random.randint(1000,9999))+'@gmail.com'

            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for i in range(8))


            w = csv.writer(f, delimiter=',')
            w.writerow([id, email, password, fname, lname, address, balance])

def createBuyers():
    with open(db + 'Buyer.csv', mode='w') as f:
        for i in range(301):
            w = csv.writer(f, delimiter=',')
            w.writerow([i])

def createSellers():
    stores = ['All Things More', 'Beautiful Charm', 'Ambrosia Store', 'African Paradise', 'Alike Desire', 'All My Grace', 'American Eagle Shop', 'Actioner Sports Store', 'Adaline’s Wardrobe', 'Addiction Like', 'American Blues', 'Ancient Crust', 'Ancient Grounds', 'Angelic Threads', 'Anytime Buys', 'Apple Alley', 'Apple Blossoms', 'Apple Grand Central', 'Around The Clock Shop', 'Authentic Shoppe', 'BALENCIAGA', 'Balsamic', 'Banana Wear', 'Baskets Of Berries', 'Bayside Cavern', 'Bean Box', 'Beef Quest', 'Bella Bella Boutique', 'Bend the Trend', 'Berries And Bushes', 'Berries Galore', 'Berry Farm', 'Berry Land', 'Best Discount', 'Best Indulgence', 'Best Mart', 'Best of Harvests', 'Best Price', 'BestBuy', 'Bestir Service', 'Better Buys', 'Bien Habillé', 'Big Mall', 'Big Mart', 'Bikini Beans', 'Billowy Love', 'Bitternut', 'Black Eye Coffee', 'Blackbird Boutique', 'Blacklight Clothing', 'Blessed Bounty', 'Blessed Fruits', 'Bloomingdale’s', 'Blue Diamond', 'Blue Mall', 'Blue Market', 'Blue Shelves', 'Blueberry Bean', 'Bluebill Open mall', 'Bluebird Store', 'Blush Boutique', 'Body Canvas', 'Bon Comida', 'Bookstore', 'Boomers Apparel', 'Bountiful Berries', 'Boutique de Paris', 'Brandy Melville', 'Brick And Cyber', 'Bruno’s Groceries', 'Budding Business', 'Budget Banquet', 'Budget Beauty', 'Bumble Bee Boutique', 'Bunny Shop', 'Burger Garden', 'Burgundy Boutique', 'Burlington', 'Burly Giggles', 'Bursting Baskets', 'Bursting With Fruit', 'Burton', 'Business Bustle', 'Butter Buds', 'By the Handful', 'Cafe Corner Shots', 'Cafe Linger', 'Calm Charm', 'Calm Glitter', 'Campfire Clothes', 'Carbonated Corner', 'Careful Dishing', 'Carmine', 'Catered Care', 'Cavern Cooks', 'Celestial Citrus Farms', 'Changing Seasons', 'Chapeau Chic', 'Chaperon', 'Charlie’s Retail', 'Charm Farm', 'Charming Charlotte', 'Chateaux', 'Cheat on Wheels', 'Cheeky Chic', 'Cheereal', 'Chef Naturelle', 'Chic Château', 'Choose And Track', 'Chowhound']

    storeslst = []
    with open(db + 'Seller.csv', mode='w') as f:
        for i in range(200):
            id = i
            store = random.choice(stores) + str(random.randint(100,999))

            if store not in storeslst:
                storeslst.append(store)
                w = csv.writer(f, delimiter=',')
                w.writerow([id, store])

def createProducts():
    colors=['red', 'green', 'blue', 'teal', 'orange', 'yellow', 'maroon', 'pink', 'lilac', 'rose', 'magenta', 'rust', 'burgundy', 'grass', 'lime', 'lemon', 'white', 'cream', 'indigo', 'purple', 'oatmeal', 'beige', 'black', 'grey', 'charcoal', 'tin', 'gold', 'silver', 'brick', 'blush', 'khaki', 'violet', 'coral', 'salmon', 'brown', 'bronze', 'tan']

    qualities=['latest', 'older', 'vintage','shiny', 'dull', 'matte', 'nice', 'good', 'great', 'quality', '5star', 'best', 'cool']

    category=['books', 'clothes', 'household', 'electronics', 'health']

    books=['The Abbey Series', 'Biggles Flies East', 'Billy Bunter of Greyfriars School','Brendon Chase', 'The Camels Are Coming', 'Dimsie Goes To School', 'Dimsie Moves Up', 'The Story of Doctor Dolittle', 'Five Children and It', 'Five on a Treasure Island', 'The Hobbit', 'The House at Pooh Corner', 'Just Jane', 'Just William', 'The Little Grey Men', 'The Little Lost Hen', 'A Little Princess', 'The Lord of the Rings', 'The Fellowship of the Ring', 'The Two Towers', 'The Return of the King', 'The Lost Prince', '"The Little Bookroom', 'The Magic World', 'Meredith and Co.', 'No Boats on Bannermere', 'The Mystery of the Burnt Cottage', "Old Peter's Russian Tales", 'The Once and Future King', 'The Sword in the Stone', 'The Queen of Air and Darkness', 'The Ill-Made Knight', 'The Candle in the Wind', 'Peter and Wendy', 'Peter Pan in Kensington Gardens', 'The Phoenix and the Carpet', 'A Popular Schoolgirl', 'The Railway Children', 'The School at the Chalet', 'The Secret Garden', 'The Squirrel, The Hare and the Little Grey Rabbit', 'The Story of the Amulet', 'Swallows and Amazons series', 'Swallows and Amazons', 'Swallowdale', 'The Tailor of Gloucester', 'The Tale of Mrs. Tiggy-Winkle', 'The Tale of Peter Rabbit', 'The Tale of Squirrel Nutkin', 'The Tale of the Pie and the Patty-Pan', 'The Tale of Tom Kitten', 'The Wind in the Willows', 'Winnie-the-Pooh']

    clothes=['pants', 'dress', 'shirt', 'tshirt', 'buttondown', 'buttonup', 'blazer', 'suit', 'trousers', 'slacks', 'socks', 'ties', 'bandanas', 'belt', 'shoes', 'chinos', 'khakis', 'sweater', 'crewneck', 'sweatshirts', 'jogger', 'legging', 'shorts', 'jacket', 'hoody', 'slippers', 'boots', 'booties', 'raincoat', 'camisole', 'longsleeveshirt', 'jeans', 'jorts', 'jegging', 'tanktop']

    household=['spoon', 'fork', 'knife', 'chair', 'sofa', 'table', 'vase', 'flower', 'countertop', 'desk', 'lamp', 'lightbulb', 'charger', 'phone', 'waterbottle', 'brita', 'can', 'glass', 'plate', 'bowl', 'dish', 'spatula', 'oven', 'dishwasher', 'sink', 'faucet', 'soap', 'dishsoap', 'coffee', 'grinder', 'whisk', 'toaster', 'fryer', 'ladle', 'mitts', 'rack', 'candle', 'lighter', 'cork', 'coaster', 'peeler', 'smasher', 'cup', 'brush', 'bag', 'shelf', 'couch', 'painting', 'barstool', 'stool', 'footrest', 'sectional', 'endpiece', 'bookshelf', 'rug', 'mattress', 'bedframe', 'strainer', 'sieve', 'mixer']

    electronics= ['microwave', 'television', 'phone', 'landline', 'gadget', 'cord', 'dongle', 'protector', 'case', 'battery', 'lithium', 'watch', 'computer', 'laptop', 'cable', 'camera', 'speaker', 'headset', 'earphones', 'earbuds', 'boombox', 'monitor', 'projector', 'soundstation', 'soundbox', 'desktop', 'harddrive', 'keyboard', 'mouse', 'mousepad', 'router']

    health=['toothbrush', 'retainer', 'flosser', 'floss', 'soap', 'shampoo', 'conditioner', 'gel', 'pomade', 'mousse', 'hairspray', 'volumizer', 'hairbrush', 'mask', 'vitamin', 'tablet', 'pill', 'cream', 'lotion', 'moisturizer', 'supplement', 'dumbbell', 'kettlebell', 'foamroller', 'ball', 'hulahoop', 'mat', 'foambloack', 'yogamat', 'bar']

    products = []
    avail_prods = []
    with open(db + 'Product.csv', mode='w') as f:
        for i in range(250):
            name = random.choice(colors)+" "+random.choice(qualities)+" "+random.choice(books)+" book"
            cat = 'books'
            url = 'url'
            avail = random.choice([True, False])
            desc = name

            if name not in products:
                products.append(name)
                if avail == True:
                    avail_prods.append(name)
                w = csv.writer(f, delimiter=',')
                w.writerow([name, cat, url, avail, desc])

        for i in range(250):
            name = random.choice(colors)+" "+random.choice(qualities)+" "+random.choice(household)
            cat = 'household'
            url = 'url'
            avail = random.choice([True, False])
            desc = name

            if name not in products:
                products.append(name)
                if avail == True:
                    avail_prods.append(name)
                w = csv.writer(f, delimiter=',')
                w.writerow([name, cat, url, avail, desc])

        for i in range(250):
            name = random.choice(colors)+" "+random.choice(qualities)+" "+random.choice(clothes)
            cat = 'clothes'
            url = 'url'
            avail = random.choice([True, False])
            desc = name

            if name not in products:
                products.append(name)
                if avail == True:
                    avail_prods.append(name)
                w = csv.writer(f, delimiter=',')
                w.writerow([name, cat, url, avail, desc])

        for i in range(250):
            name = random.choice(colors)+" "+random.choice(qualities)+" "+random.choice(electronics)
            cat = 'electronics'
            url = 'url'
            avail = random.choice([True, False])
            desc = name

            if name not in products:
                products.append(name)
                if avail == True:
                    avail_prods.append(name)
                w = csv.writer(f, delimiter=',')
                w.writerow([name, cat, url, avail, desc])

        for i in range(250):
            name = random.choice(colors)+" "+random.choice(qualities)+" "+random.choice(health)
            cat = 'health'
            url = 'url'
            avail = random.choice([True, False])
            desc = name

            if name not in products:
                products.append(name)
                if avail == True:
                    avail_prods.append(name)
                w = csv.writer(f, delimiter=',')
                w.writerow([name, cat, url, avail, desc])

    with open(db + 'Orders.csv', mode='w') as f:
        for i in range(100):
            buyer_id= random.randint(0,300)
            yr = str(random.randint(1970,2021))
            month = str("%02d" % random.randint(1,12))
            day = str("%02d" % random.randint(1,29))

            hr= str("%02d" % random.randint(1,23))
            min= str("%02d" % random.randint(1,59))
            sec= str("%02d" % random.randint(1,59))

            ts = yr+'-'+month+'-'+day+' '+hr+':'+min+':'+sec
            for num in range(random.randint(1,10)):
                seller_id = random.randint(0,199)
                prod = random.choice(products)
                status = random.choice([True, False])
                url = 'url'
                quantity = random.randint(1,10)
                final_price = random.randint(10,100)

                w = csv.writer(f, delimiter=',')
                w.writerow([buyer_id, ts, seller_id, prod, quantity, status, url, final_price])

    selllst = []
    with open(db + 'Selling.csv', mode='w') as f:
        for i in range(500):
            seller_id = random.randint(0,199)
            prod = random.choice(avail_prods)
            price = random.randint(1,1000)
            quant = random.randint(1,1000)

            if (seller_id, prod) not in selllst:
                selllst.append((seller_id, prod))
                w = csv.writer(f, delimiter=',')
                w.writerow([seller_id, prod, price, quant])

    with open(db + 'Cart.csv', mode='w') as f:
        for i in range(500):
            buyer_id= random.randint(0,300)
            seller_id = random.randint(0,199)
            prod = random.choice(products)
            quant = random.randint(1,1000)

            w = csv.writer(f, delimiter=',')
            w.writerow([buyer_id, prod, seller_id, quant])

    with open(db + 'Product_Review.csv', mode='w') as f:
        for i in range(500):
            buyer_id= random.randint(0,299)
            prod = random.choice(products)
            rating = random.randint(1,100)
            upvote = random.randint(1,100)
            downvote = random.randint(1,100)

            yr = str(random.randint(1970,2021))
            month = str("%02d" % random.randint(1,12))
            day = str("%02d" % random.randint(1,29))

            date = yr+'-'+month+'-'+day

            w = csv.writer(f, delimiter=',')
            w.writerow([prod, buyer_id, rating, date, upvote, downvote])

createUser()
createBuyers()
createSellers()
createProducts()
