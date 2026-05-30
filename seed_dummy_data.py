import os
import sys
import re

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Load the backend/.env file explicitly so pydantic finds it
from dotenv import load_dotenv
load_dotenv(os.path.join(backend_dir, ".env"))

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text).strip('-')

from app.database.connection import SessionLocal
from app.models.category import Category
from app.models.product import Product

def seed_dummy_data():
    db = SessionLocal()
    try:
        # 1. Dummy Categories
        categories_data = [
            {"name": "Industrial Valves", "image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80"},
            {"name": "Pipes & Fittings", "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80"},
            {"name": "Heavy Machinery Parts", "image": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=800&q=80"},
            {"name": "Safety Equipment", "image": "https://images.unsplash.com/photo-1579847188729-e85d68128ec9?w=800&q=80"},
            {"name": "Electrical Components", "image": "https://images.unsplash.com/photo-1620288627223-53302f4e8c74?w=800&q=80"}
        ]
        
        category_objects = []
        for cat_info in categories_data:
            slug = slugify(cat_info["name"])
            cat = db.query(Category).filter(Category.slug == slug).first()
            if not cat:
                cat = Category(
                    name=cat_info["name"], 
                    slug=slug,
                    image=cat_info["image"]
                )
                db.add(cat)
                db.commit()
                db.refresh(cat)
                print(f"✅ Created category: {cat.name}")
            else:
                print(f"ℹ️ Category already exists: {cat.name}")
            category_objects.append(cat)
            
        # 2. Dummy Products
        products_data = [
            {
                "name": "High-Pressure Gate Valve",
                "cat_idx": 0,
                "sku": "VAL-1001",
                "short_desc": "Industrial grade high-pressure gate valve for pipeline applications.",
                "desc": "Constructed from forged steel, this gate valve ensures reliable shutoff in high-pressure environments. Ideal for oil, gas, and water applications. Features rising stem design.",
                "moq": 50,
                "featured": True,
                "image": "https://images.unsplash.com/photo-1581092335397-9583eb92d232?w=800&q=80",
                "gallery": ["https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&q=80"]
            },
            {
                "name": "Stainless Steel Check Valve",
                "cat_idx": 0,
                "sku": "VAL-1002",
                "short_desc": "Corrosion-resistant stainless steel check valve.",
                "desc": "Prevents backflow in piping systems. Manufactured with 316L stainless steel for maximum durability in harsh chemical environments.",
                "moq": 100,
                "featured": False,
                "image": "https://images.unsplash.com/photo-1621873130456-0775d7b5b5c9?w=800&q=80",
                "gallery": []
            },
            {
                "name": "Seamless Carbon Steel Pipe",
                "cat_idx": 1,
                "sku": "PIP-2001",
                "short_desc": "Heavy-duty seamless carbon steel pipe for industrial use.",
                "desc": "Available in various diameters and thicknesses. Conforms to ASTM A106 Grade B standards. High temperature and high pressure resistant.",
                "moq": 500,
                "featured": True,
                "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80",
                "gallery": []
            },
            {
                "name": "Industrial Safety Helmet",
                "cat_idx": 3,
                "sku": "SAF-4001",
                "short_desc": "High-impact resistant industrial safety helmet.",
                "desc": "Features adjustable suspension and ventilation. Meets ANSI Z89.1 standards for impact protection. Available in multiple high-visibility colors.",
                "moq": 200,
                "featured": True,
                "image": "https://images.unsplash.com/photo-1579847188729-e85d68128ec9?w=800&q=80",
                "gallery": []
            },
            {
                "name": "Three-Phase Industrial Motor",
                "cat_idx": 4,
                "sku": "ELE-5001",
                "short_desc": "High-efficiency three-phase induction motor.",
                "desc": "Provides reliable power for heavy machinery. Features IP55 enclosure protection against dust and water jets. TEFC cooling system.",
                "moq": 10,
                "featured": True,
                "image": "https://images.unsplash.com/photo-1620288627223-53302f4e8c74?w=800&q=80",
                "gallery": []
            }
        ]
        
        for pd in products_data:
            slug = slugify(pd["name"])
            prod = db.query(Product).filter(Product.slug == slug).first()
            if not prod:
                prod = Product(
                    category_id=category_objects[pd["cat_idx"]].id,
                    name=pd["name"],
                    slug=slug,
                    sku=pd["sku"],
                    short_description=pd["short_desc"],
                    description=pd["desc"],
                    moq=pd["moq"],
                    featured=pd["featured"],
                    stock_status="in_stock",
                    image=pd["image"],
                    gallery_images=pd["gallery"]
                )
                db.add(prod)
                db.commit()
                print(f"✅ Created product: {pd['name']}")
            else:
                print(f"ℹ️ Product already exists: {pd['name']}")
                
        print("\n🎉 Dummy data seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_dummy_data()
