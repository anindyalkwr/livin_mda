CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(100) NOT NULL,
    address TEXT,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL,
    balance NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    living_points INTEGER NOT NULL DEFAULT 0,
    holded_balance NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE merchants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    label VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    merchant_id UUID REFERENCES merchants(id) ON DELETE SET NULL,
    amount NUMERIC(15, 2) NOT NULL, -- Increased precision for Rupiah
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE offers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    product_id UUID REFERENCES products(id),
    quantity INTEGER,
    total_amount NUMERIC(15, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    transaction_type VARCHAR(20) NOT NULL,
    transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION create_user_account()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO accounts(user_id) VALUES(NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER create_account_trigger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION create_user_account();



INSERT INTO merchants (id, name) VALUES
(uuid_generate_v4(), 'TokoPedia'),
(uuid_generate_v4(), 'Bhinneka'),
(uuid_generate_v4(), 'Gramedia'),
(uuid_generate_v4(), 'Indomaret'),
(uuid_generate_v4(), 'Uniqlo Indonesia'),
(uuid_generate_v4(), 'IKEA Indonesia');

INSERT INTO categories (id, label) VALUES
(uuid_generate_v4(), 'Elektronik'),
(uuid_generate_v4(), 'Sembako'),
(uuid_generate_v4(), 'Buku & Majalah'),
(uuid_generate_v4(), 'Pakaian'),
(uuid_generate_v4(), 'Dapur & Rumah Tangga'),
(uuid_generate_v4(), 'Kesehatan & Kecantikan'),
(uuid_generate_v4(), 'Mainan & Hobi');

DO $$
DECLARE
    cat_elektronik_id UUID := (SELECT id FROM categories WHERE label = 'Elektronik');
    cat_sembako_id UUID := (SELECT id FROM categories WHERE label = 'Sembako');
    cat_buku_id UUID := (SELECT id FROM categories WHERE label = 'Buku & Majalah');
    cat_pakaian_id UUID := (SELECT id FROM categories WHERE label = 'Pakaian');
    cat_dapur_id UUID := (SELECT id FROM categories WHERE label = 'Dapur & Rumah Tangga');
    cat_kesehatan_id UUID := (SELECT id FROM categories WHERE label = 'Kesehatan & Kecantikan');
    cat_hobi_id UUID := (SELECT id FROM categories WHERE label = 'Mainan & Hobi');

    merch_tokped_id UUID := (SELECT id FROM merchants WHERE name = 'TokoPedia');
    merch_bhinneka_id UUID := (SELECT id FROM merchants WHERE name = 'Bhinneka');
    merch_gramed_id UUID := (SELECT id FROM merchants WHERE name = 'Gramedia');
    merch_indomaret_id UUID := (SELECT id FROM merchants WHERE name = 'Indomaret');
    merch_uniqlo_id UUID := (SELECT id FROM merchants WHERE name = 'Uniqlo Indonesia');
    merch_ikea_id UUID := (SELECT id FROM merchants WHERE name = 'IKEA Indonesia');
BEGIN
    INSERT INTO products (name, category_id, merchant_id, amount, stock) VALUES
    ('Samsung Galaxy S25', cat_elektronik_id, merch_tokped_id, 18500000.00, 150),
    ('Laptop ASUS ROG Zephyrus', cat_elektronik_id, merch_bhinneka_id, 32000000.00, 75),
    ('Sony Alpha A7 IV Camera', cat_elektronik_id, merch_bhinneka_id, 35000000.00, 40),
    ('Minyak Goreng Sania 2L', cat_sembako_id, merch_indomaret_id, 35000.00, 1500),
    ('Beras Rojolele 5kg', cat_sembako_id, merch_indomaret_id, 68000.00, 1200),
    ('Indomie Goreng (1 dus)', cat_sembako_id, merch_indomaret_id, 105000.00, 2000),
    ('Buku "Laskar Pelangi" by Andrea Hirata', cat_buku_id, merch_gramed_id, 95000.00, 500),
    ('Buku "Atomic Habits" (Terjemahan)', cat_buku_id, merch_gramed_id, 108000.00, 600),
    ('Uniqlo T-Shirt AIRism', cat_pakaian_id, merch_uniqlo_id, 199000.00, 800),
    ('Celana Chino Pria', cat_pakaian_id, merch_uniqlo_id, 499000.00, 650),
    ('Rak Buku IKEA BILLY', cat_dapur_id, merch_ikea_id, 899000.00, 200),
    ('Panci Set Maxim', cat_dapur_id, merch_tokped_id, 350000.00, 300),
    ('SK-II Facial Treatment Essence', cat_kesehatan_id, merch_tokped_id, 2850000.00, 100),
    ('Lego Star Wars Millennium Falcon', cat_hobi_id, merch_tokped_id, 12500000.00, 25);
END $$;


DO $$
DECLARE
    cat_elektronik_id UUID := (SELECT id FROM categories WHERE label = 'Elektronik');
    cat_sembako_id UUID := (SELECT id FROM categories WHERE label = 'Sembako');
    cat_buku_id UUID := (SELECT id FROM categories WHERE label = 'Buku & Majalah');
BEGIN
    INSERT INTO offers (name, description, category_id) VALUES
    ('Diskon Gajian Elektronik', 'Diskon hingga 2 Juta untuk semua produk elektronik.', cat_elektronik_id),
    ('Promo Jumat Berkah Sembako', 'Beli 2 gratis 1 untuk produk sembako pilihan.', cat_sembako_id),
    ('Gramedia Book Fair Online', 'Diskon 30% untuk semua buku terbitan Gramedia.', cat_buku_id);
END $$;
 