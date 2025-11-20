-- To restore the PostgreSQL databases :
-- 1) Create a new database in PostgreSQL with the name 'ProjectDB'
-- 2) Locate the Tables section in the newly created database and open the Query Tool.
-- 3) Run the following commands in the Query Tool:

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username TEXT NOT NULL,
    country TEXT NOT NULL,
    level INT NOT NULL
);

INSERT INTO users (user_id, username, country, level) VALUES
(1, 'Haven', 'Finland', 25),
(2, 'Viper', 'Germany', 34),
(3, 'G1su', 'Sweden', 26),
(4, 'Jojo', 'Spain', 13),
(5, 'Falco', 'Norway', 7),
(6, 'Stolen', 'UK', 72),
(7, 'Beefy', 'Poland', 45),
(8, 'Hustler', 'Ireland', 24),
(9, 'Scyptic', 'Switzerland', 6),
(10, 'Pallokala', 'Finland', 15),
(11, 'Revan', 'Italy', 54),
(12, 'Lemari', 'Russia', 23),
(13, 'I_Love_USA', 'USA', 61),
(14, 'firewalker', 'Austria', 4),
(15, 'Fihoo', 'Norway', 16);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quality TEXT NOT NULL
);

INSERT INTO products VALUES
(1, 'Iron Sword', 'Weapons', 29.99, 'medium'),
(2, 'Steel Shield', 'Armor', 39.99, 'high'),
(3, 'Magic Scroll', 'Magic', 19.99, 'low'),
(4, 'Healing Potion', 'Consumables', 9.99, 'high'),
(5, 'Battle Axe', 'Weapons', 34.99, 'medium'),
(6, 'Longbow', 'Weapons', 49.99, 'high'),
(7, 'Dragon Helm', 'Armor', 79.99, 'high'),
(8, 'Dagger', 'Weapons', 14.99, 'low'),
(9, 'Golden Armor', 'Armor', 199.99, 'high'),
(10, 'Revolver', 'Weapons', 59.99, 'medium'),
(11, 'First Aid Kit', 'Consumables', 12.99, 'medium'),
(12, 'Energy Drink', 'Consumables', 4.99, 'low'),
(13, 'Tactical Vest', 'Armor', 89.99, 'high'),
(14, 'Flash Grenade', 'Gear', 24.99, 'low'),
(15, 'Katana', 'Weapons', 149.99, 'high');

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO orders VALUES
(1, 1, 1, 2),
(2, 2, 2, 1),
(3, 3, 4, 5),
(4, 4, 6, 1),
(5, 5, 5, 1),
(6, 6, 10, 2),
(7, 7, 3, 3),
(8, 8, 11, 1),
(9, 9, 7, 1),
(10, 10, 12, 4),
(11, 11, 13, 1),
(12, 12, 8, 2),
(13, 13, 15, 1),
(14, 14, 14, 3),
(15, 15, 9, 1);

CREATE TABLE achievements (
    achievement_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT NOT NULL,
    points INT NOT NULL 
);

INSERT INTO achievements VALUES
(1, 1, 'First Blood', 10),
(2, 2, 'Explorer', 20),
(3, 3, 'Treasure Hunter', 15),
(4, 4, 'Champion', 25),
(5, 5, 'Master Crafter', 30),
(6, 6, 'Speed Runner', 18),
(7, 7, 'Sharpshooter', 22),
(8, 8, 'Defender', 16),
(9, 9, 'Beast Slayer', 24),
(10, 10, 'Strategist', 28),
(11, 11, 'Gladiator', 35),
(12, 12, 'Medic', 12),
(13, 13, 'Samurai Spirit', 40),
(14, 14, 'Tank', 19),
(15, 15, 'Hero of the Realm', 50);

CREATE TABLE comments (
    comment_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    total_length INT NOT NULL CHECK (total_length >= 0),
    published_at TEXT NOT NULL,
    likes INT NOT NULL CHECK (likes >= 0)
);

INSERT INTO comments VALUES
(1, 1, 120, '2024-01-10', 5),
(2, 2, 45, '2024-01-11', 2),
(3, 3, 89, '2024-01-12', 3),
(4, 4, 150, '2024-01-13', 8),
(5, 5, 72, '2024-01-14', 1),
(6, 6, 38, '2024-01-15', 0),
(7, 7, 165, '2024-01-16', 9),
(8, 8, 60, '2024-01-17', 4),
(9, 9, 57, '2024-01-18', 2),
(10, 10, 200, '2024-01-19', 10),
(11, 11, 118, '2024-01-20', 5),
(12, 12, 48, '2024-01-21', 1),
(13, 13, 75, '2024-01-22', 3),
(14, 14, 100, '2024-01-23', 4),
(15, 15, 32, '2024-01-24', 0);

