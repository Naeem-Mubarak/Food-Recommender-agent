from database.db_connection import db_connection
from config.system_info import DB_PATH


cursor , conn =db_connection(DB_PATH)


cursor.executescript("""
INSERT INTO restaurants (branch_id, name, cuisine_type) VALUES
(1, 'Spice Avenue', 'Pakistani'),
(2, 'Urban Bites', 'Fast Food'),
(3, 'Karachi Grill', 'BBQ'),
(4, 'Green Bowl', 'Healthy'),
(5, 'Pasta House', 'Italian'),
(6, 'Tokyo Kitchen', 'Japanese'),
(7, 'Texas Steakhouse', 'American'),
(8, 'Mediterranean Table', 'Mediterranean'),
(9, 'Mexican Fiesta', 'Mexican'),
(10, 'Sweet Corner', 'Desserts');


INSERT INTO dishes
(dish_id, restaurant_id, name, spice, sweet_level, price, type_of_food, healthy_rating, popularity_score)
VALUES
(1, 1, 'Chicken Biryani', 4, 0, 450, 'Non-Veg', 6, 9.5),
(2, 1, 'Chicken Karahi', 5, 0, 850, 'Non-Veg', 5, 9.2),
(3, 1, 'Chicken Handi', 3, 0, 750, 'Non-Veg', 6, 8.7),
(4, 2, 'Zinger Burger', 3, 0, 550, 'Non-Veg', 4, 9.6),
(5, 2, 'Chicken Pizza', 2, 0, 700, 'Non-Veg', 5, 8.9),
(6, 2, 'Loaded Fries', 2, 0, 400, 'Veg', 3, 8.5),
(7, 3, 'Seekh Kabab', 4, 0, 500, 'Non-Veg', 7, 9.0),
(8, 3, 'Chicken Tikka', 4, 0, 600, 'Non-Veg', 8, 9.4),
(9, 3, 'Beef Bihari Kabab', 5, 0, 750, 'Non-Veg', 6, 8.8),
(10, 4, 'Chicken Salad', 1, 0, 450, 'Non-Veg', 10, 8.8),
(11, 4, 'Grilled Chicken Bowl', 2, 0, 650, 'Non-Veg', 9, 9.1),
(12, 4, 'Vegetable Wrap', 1, 0, 350, 'Veg', 10, 8.4),
(13, 4, 'Quinoa Vegetable Bowl', 1, 0, 600, 'Veg', 10, 8.6),
(14, 4, 'Grilled Fish Salad', 1, 0, 750, 'Non-Veg', 10, 9.0),
(15, 4, 'Avocado Chickpea Salad', 1, 0, 550, 'Veg', 10, 8.5),
(16, 5, 'Chicken Alfredo', 2, 0, 850, 'Non-Veg', 6, 9.3),
(17, 5, 'Arrabbiata Pasta', 4, 0, 750, 'Veg', 7, 8.6),
(18, 5, 'Margherita Pizza', 1, 0, 650, 'Veg', 7, 8.8),
(19, 6, 'Chicken Teriyaki', 1, 2, 750, 'Non-Veg', 7, 9.0),
(20, 6, 'Chicken Ramen', 3, 0, 800, 'Non-Veg', 7, 9.2),
(21, 6, 'Vegetable Sushi', 1, 0, 650, 'Veg', 9, 8.7),
(22, 7, 'Grilled Beef Steak', 2, 0, 1400, 'Non-Veg', 7, 9.5),
(23, 7, 'Grilled Chicken', 1, 0, 850, 'Non-Veg', 9, 9.0),
(24, 7, 'Beef Burger', 2, 0, 700, 'Non-Veg', 5, 9.1),
(25, 8, 'Chicken Shawarma', 2, 0, 500, 'Non-Veg', 8, 9.3),
(26, 8, 'Falafel Plate', 1, 0, 450, 'Veg', 9, 8.8),
(27, 8, 'Hummus with Pita', 1, 0, 400, 'Veg', 9, 8.5),
(28, 9, 'Chicken Tacos', 4, 0, 600, 'Non-Veg', 7, 9.2),
(29, 9, 'Beef Burrito', 3, 0, 700, 'Non-Veg', 6, 8.9),
(30, 9, 'Mexican Rice Bowl', 3, 0, 550, 'Veg', 8, 8.7),
(31, 9, 'Grilled Chicken Fajita Bowl', 2, 0, 650, 'Non-Veg', 9, 8.9),
(32, 9, 'Black Bean Salad', 2, 0, 450, 'Veg', 10, 8.3),
(33, 10, 'Chocolate Cake', 1, 5, 450, 'Veg', 4, 9.4),
(34, 10, 'Strawberry Cheesecake', 1, 4, 500, 'Veg', 5, 9.1),
(36, 10, 'Chocolate Brownie', 1, 5, 350, 'Veg', 4, 9.3),
(37, 10, 'Caramel Pudding', 1, 5, 400, 'Veg', 5, 8.9),
(38, 10, 'Mango Cheesecake', 1, 5, 550, 'Veg', 6, 9.0),
(39, 10, 'Chocolate Fudge Cake', 1, 5, 500, 'Veg', 3, 9.5),
(40, 10, 'Gulab Jamun', 1, 5, 300, 'Veg', 6, 9.6),
(41, 10, 'Rice Pudding', 1, 5, 350, 'Veg', 7, 8.8),
(42, 10, 'Fruit Custard', 1, 5, 400, 'Veg', 8, 8.7),
(43, 10, 'Mango Ice Cream', 1, 5, 350, 'Veg', 6, 9.2),
(35, 10, 'Vanilla Ice Cream', 1, 4, 300, 'Veg', 6, 8.9);


INSERT INTO users (cust_id, name) VALUES
(1, 'James'),
(2, 'William'),
(3, 'Emma'),
(4, 'Benjamin'),
(5, 'Olivia'),
(6, 'Daniel'),
(7, 'Sophia'),
(8, 'Henry');


INSERT INTO user_data
(order_id, user_id, rest_id, dish_id, name, spice, sweet, price, type_of_food, healthy_rating)
VALUES
(1, 1, 1, 1, 'Chicken Biryani', 4, 0, 450, 'Non-Veg', 6),
(2, 1, 3, 8, 'Chicken Tikka', 4, 0, 600, 'Non-Veg', 8),
(3, 1, 2, 4, 'Zinger Burger', 3, 0, 550, 'Non-Veg', 4),
(4, 2, 1, 2, 'Chicken Karahi', 5, 0, 850, 'Non-Veg', 5),
(5, 2, 3, 9, 'Beef Bihari Kabab', 5, 0, 750, 'Non-Veg', 6),
(6, 2, 5, 17, 'Arrabbiata Pasta', 4, 0, 750, 'Veg', 7),
(7, 3, 4, 10, 'Chicken Salad', 1, 0, 450, 'Non-Veg', 10),
(8, 3, 4, 11, 'Grilled Chicken Bowl', 2, 0, 650, 'Non-Veg', 9),
(9, 3, 4, 12, 'Vegetable Wrap', 1, 0, 350, 'Veg', 10),
(10, 4, 2, 4, 'Zinger Burger', 3, 0, 550, 'Non-Veg', 4),
(11, 4, 2, 6, 'Loaded Fries', 2, 0, 400, 'Veg', 3),
(12, 4, 3, 7, 'Seekh Kabab', 4, 0, 500, 'Non-Veg', 7),
(13, 5, 4, 10, 'Chicken Salad', 1, 0, 450, 'Non-Veg', 10),
(14, 5, 5, 18, 'Margherita Pizza', 1, 0, 650, 'Veg', 7),
(15, 5, 4, 12, 'Vegetable Wrap', 1, 0, 350, 'Veg', 10),
(16, 6, 1, 1, 'Chicken Biryani', 4, 0, 450, 'Non-Veg', 6),
(17, 6, 1, 2, 'Chicken Karahi', 5, 0, 850, 'Non-Veg', 5),
(18, 6, 3, 8, 'Chicken Tikka', 4, 0, 600, 'Non-Veg', 8),
(19, 7, 5, 16, 'Chicken Alfredo', 2, 0, 850, 'Non-Veg', 6),
(20, 7, 4, 11, 'Grilled Chicken Bowl', 2, 0, 650, 'Non-Veg', 9),
(21, 7, 2, 5, 'Chicken Pizza', 2, 0, 700, 'Non-Veg', 5),
(22, 8, 3, 7, 'Seekh Kabab', 4, 0, 500, 'Non-Veg', 7),
(23, 8, 1, 3, 'Chicken Handi', 3, 0, 750, 'Non-Veg', 6),
(24, 8, 2, 4, 'Zinger Burger', 3, 0, 550, 'Non-Veg', 4);
""")

print("Data inserted Successfully")

conn.commit()
conn.close()