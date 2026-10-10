from django.core.management.base import BaseCommand
from django.core.files import File
from GoShop.models import *


class Command(BaseCommand):
    help = 'insert the category data'

    def handle(self, *args, **kwargs):

        names = [
            "Shoes",
            "T-Shirts",
            "Jeans",
            "Watches",
            "Mobiles",
            "Laptops",
            "Headphones",
            "Bags",
            "Sunglasses",
            "Sports Equipment"
        ]

        descriptions = [
            "All types of shoes",
            "Stylish t-shirts",
            "Denim and casual jeans",
            "Smart and analog watches",
            "Latest smartphones",
            "High performance laptops",
            "Wireless and wired headphones",
            "Travel and school bags",
            "Trendy sunglasses",
            "All sports items"
        ]

        images = [
            "media/upload/shoes.jpg",
            "media/upload/tshirts.jpg",
            "media/upload/jeans.jpg",
            "media/upload/watches.jpg",
            "media/upload/mobiles.jpg",
            "media/upload/laptops.jpg",
            "media/upload/headphones.jpg",
            "media/upload/bags.jpg",
            "media/upload/sunglasses.jpg",
            "media/upload/sports.jpg"
        ]

        status_list = [
            False, False, False, False, False,
            False, False, False, False, False
        ]

        created_at_list = [
            "Dinesh",
            "Arun",
            "Karthik",
            "Vijay",
            "Ajith",
            "Rahul",
            "Suresh",
            "Praveen",
            "Manoj",
            "Rakesh"
        ]

        for name, des, img, status, create in zip(
            names,
            descriptions,
            images,
            status_list,
            created_at_list
        ):

            if not Category.objects.filter(name=name).exists():

                with open(img, 'rb') as f:

                    Category.objects.create(
                        name=name,
                        description=des,
                        image=File(f),
                        status=status,
                        created_at=create,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Categories inserted successfully!"
            )
        )