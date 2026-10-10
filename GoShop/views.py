from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .forms import UserSignUp
from django.http import JsonResponse


class Home(View):
    def get(self,request):
        hot=Product.objects.filter(trending=1,status=0,category__status=0)
        list_Category=Category.objects.filter(status=0)
        ft=FeedBack.objects.all()
        fav=favourate.objects.all()
        if request.user.is_authenticated:
           liked_products = set(
               favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True)
           )
           no_fav = len(liked_products)
        else:
           liked_products = set()
           no_fav = 0
        if not hot.exists():
           messages.warning(request,'can find the product')
           exit
        return render (request,'frontend/Landing_Page.html',{'hot':hot,'mes':messages,'list_Category':list_Category,'ft':ft,'fav':fav,'liked_products':liked_products,'no_fav':no_fav})

# class Category_View(View):
#     def get(Selft,request):
#         list_Product=Category.objects.all()
#         return render(request,'frontend/Category.html',{'list':list_Product})

# class Product_View(View):
#     def get(self,request,name):
#         pro=Product.objects.filter(category__name=name)
#         return render(request,'frontend/Product.html',{'pro':pro})
    
# class product_all(View):
#     def get(self,request):
#         all_products=Product.objects.filter(status=0)
#         return render(request,'frontend/all_products.html',{'all_products':all_products})
    
# class product_page(View):
#       def get(self,request,id):
#           fil=get_object_or_404(Product, id=id)
#           Related_Product=Product.objects.filter(category=fil.category).exclude(id=fil.id)
#           if request.user.is_authenticated:
#              liked_products = favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True)
#           else:
#              liked_products = []

#           return render(request,'frontend/product_page.html',{'product':fil,'related':Related_Product,'liked_products':liked_products},)
class Category_View(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        sort = request.GET.get('sort')

        if sort == 'low':
            products = products.order_by('selling_price')
        elif sort == 'high':
            products = products.order_by('-selling_price')
        elif sort == 'hot':
            products = products.filter(trending=True)

        if request.user.is_authenticated:
            liked_products = set(favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True))
        else:
            liked_products = set()

        return render(request, 'frontend/Product_List_page.html', {
            'list': categories,
            'pro': products,
            'category_name': None,
            'liked_products': liked_products
        })
class Product_View(View):
    def get(self, request, name):
        categories = Category.objects.all()
        products = Product.objects.filter(category__name=name)
        sort = request.GET.get('sort')

        if sort == 'low':
            products = products.order_by('selling_price')
        elif sort == 'high':
            products = products.order_by('-selling_price')
        elif sort == 'hot':
            products = products.filter(trending=True)


        if request.user.is_authenticated:
            liked_products = set(favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True))
        else:
            liked_products = set()

        return render(request, 'frontend/Product_List_page.html', {
            'list': categories,
            'pro': products,
            'category_name': name,
            'liked_products': liked_products
        })
class product_all(View):
    def get(self,request):
        all_products=Product.objects.filter(status=0)
        return render(request,'frontend/all_products.html',{'all_products':all_products})
    
# class product_page(View):
#       def get(self,request,id):
#           fil=get_object_or_404(Product, id=id)
#           Related_Product=Product.objects.filter(category=fil.category).exclude(id=fil.id)
#           if request.user.is_authenticated:
#              liked_products = favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True)
#           else:
#              liked_products = []

#           return render(request,'frontend/product_page.html',{'product':fil,'related':Related_Product,'liked_products':liked_products},)

class product_page(View):
      def get(self,request,id):
          fil=get_object_or_404(Product, id=id)
          Related_Product=Product.objects.filter(category=fil.category).exclude(id=fil.id)
          if request.user.is_authenticated:
             liked_products = favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True)
          else:
             liked_products = []

          return render(request,'frontend/Selected_Product_page.html',{'product':fil,'related':Related_Product,'liked_products':liked_products},)

class SignUp_Page(View):
    def get(self,request):
        form=UserSignUp()
        return render(request,'frontend/signup.html',{'form':form})
    def post(self,request):
        form=UserSignUp(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Home')

            
        return render(request,'frontend/signup.html',{'form':form})
    

class login_view(View):
    def get(self,request):
        return render(request,'frontend/login.html')
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        Aura=authenticate(request,username=username,password=password)
        if Aura is not None:
            login(request,Aura)
            return redirect('Home')
        return render(request,'frontend/login.html')
        
class logout_view(View):
    def get(self,request):
        logout(request)
        return redirect('Home')
    
class Cart_page(View):
    def post(self,request,id):
        main_id=Product.objects.get(id=id) 
        qty=int(request.POST.get('quantity'))
        Mtx=int(10)
        if qty > main_id.quantity:
            messages.error(request,'less product quantity')
            return redirect('Selected_Product',id=id)
        
        if qty < 1:
            messages.error(request,'select minimum 1 product quantity')
            return redirect('Selected_Product',id=id)
        
        cart_item,create=Cart_Page.objects.get_or_create(user=request.user,pro=main_id)

        if not create:
            cart_item.cart_quantity +=qty
        else:
            cart_item.cart_quantity = qty

        if cart_item.cart_quantity > Mtx :
            messages.error(request,f'You can add maximum {Mtx} units per product')
            return redirect('Selected_Product',id=id)
            
        
        
        cart_item.save()
        messages.success(request, "Product added to cart")
        return redirect('Selected_Product',id=id)
    
class cart_delete(View):
    def get(self,request,id):
        delete_Cart=Cart_Page.objects.get(id=id)
        delete_Cart.delete()
        return redirect('order_page')


    
class toggle_like(View):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)

        fav = favourate.objects.filter(
            user=request.user,
            pro_duct=product   # ✅ correct field
        )

        if fav.exists():
            fav.delete()   # delete from DB
        else:
            favourate.objects.create(
                user=request.user,
                pro_duct=product
            )

        return redirect(request.META.get('HTTP_REFERER','Home'))

class favourate_view(View):
    def get(self,request):
        # like_items=favourate.objects.all()
        

        if request.user.is_authenticated:
            liked_product=favourate.objects.filter(user=request.user)
        else:
            liked_product=[]
        no_fav=len(liked_product)
        return render(request,'frontend/Favourate_Page.html',{'liked_product':liked_product,'no_fav':no_fav})
        
class order_page(View):
    def get(self,request):
        if not request.user.is_authenticated:
           return redirect('login')
        total = 0
        products_order=Cart_Page.objects.filter(user=request.user)
        for i in products_order:
            i.item_total = i.pro.selling_price * i.cart_quantity
            total += i.item_total
        return render(request,'frontend/cart.html',{'products_order':products_order,'total':total})
    
# class sheping_View(View):
#     def get(self,request):
#         user=request.user
#         validit=Cart_Page.objects.filter(user=user)
#         if not validit.exists():
#             return HttpResponse('the cart is empty')
#         for items in validit:
#             print(items.pro,items.cart_quantity)
#         return render(request, "shipping.html", {"cart_items": validit})

#     def post(self,request):
#         shipping_detail=shipping.objects.filter(user=request.user).first()
        
#         user=request.user

#         fields = {
#     "user": user,
#     "full_name": request.POST.get('full_name'),
#     "email": request.POST.get('email'),
#     "phone": request.POST.get('phone'),
#     "address": request.POST.get('address'),
#     "city": request.POST.get('city'),
#     "state": request.POST.get('state'),
#     "pin_code": request.POST.get('pin_code'),
#     "landmark": request.POST.get('landmark'),
# }
#         if not shipping_detail:
#             Shipping_add=shipping.objects.create(**fields)

#         else :
#             for key,value in fields.items():
#                 setattr(shipping_detail,key,value)
                
#             shipping_detail.save()

#         # 2

#         cart_items = Cart_Page.objects.filter(user=user)
#         ship = shipping.objects.filter(user=user).first()

#         if not cart_items.exists():
#             return HttpResponse("Cart is empty")

#         if not ship:
#             return HttpResponse("Add shipping first")

#         for item in cart_items:
#             # check if delivery already exists
#             dv, created = delivery.objects.get_or_create(
#                 user=user,
#                 cart=item,
#                 defaults={"shipping_address": ship},
#                 )
#             dv.amount=item.cart_quantity * item.pro.selling_price
#             dv.save()
            
#             # if already exists → update shipping
#             if not created:
#                 dv.shipping_address = ship
#                 dv.save()
#             item.delete()

#         return redirect('order_page') 
class ShepingView(View):
    def post(self, request):
        user = request.user

        # 1️⃣ Save or update shipping info
        ship, _ = shipping.objects.update_or_create(
            user=user,
            defaults={
                "full_name": request.POST.get('full_name'),
                "email": request.POST.get('email'),
                "phone": request.POST.get('phone'),
                "address": request.POST.get('address'),
                "city": request.POST.get('city'),
                "state": request.POST.get('state'),
                "pin_code": request.POST.get('pin_code'),
                "country": request.POST.get('country'),
                "landmark": request.POST.get('landmark'),
            }
        )

        # 2️⃣ Get all cart items
        cart_items = Cart_Page.objects.filter(user=user)
        if not cart_items.exists():
            return HttpResponse("Cart is empty")

        # 3️⃣ Create delivery for each cart item
        for item in cart_items:
            dv, created = delivery.objects.get_or_create(
                user=user,
                cart=item,
                defaults={
                    "shipping_address": ship,
                    "amount": item.cart_quantity * item.pro.selling_price
                }
            )

            # If already exists, update amount and shipping
            if not created:
                dv.shipping_address = ship
                dv.amount = item.cart_quantity * item.pro.selling_price
                dv.save()

            # Delete the cart item
            item.delete()

        return redirect('order_page')
    


class ShepingView(View):
    def get(self,request):
        ship=shipping.objects.filter(user=request.user)
# Prepare values for the template
        context = {
            "full_name": ship.full_name if ship else "",
            "email": ship.email if ship else "",
            "phone": ship.phone if ship else "",
            "address": ship.address if ship else "",
            "city": ship.city if ship else "",
            "state": ship.state if ship else "",
            "pin_code": ship.pin_code if ship else "",
            "landmark": ship.landmark if ship else "",
        }
        return render(request, "shipping.html", context)
    def post(self, request):
        user = request.user

        # 1️⃣ Save or update shipping info
        ship, _ = shipping.objects.update_or_create(
            user=user,
            defaults={
                "full_name": request.POST.get('full_name'),
                "email": request.POST.get('email'),
                "phone": request.POST.get('phone'),
                "address": request.POST.get('address'),
                "city": request.POST.get('city'),
                "state": request.POST.get('state'),
                "pin_code": request.POST.get('pin_code'),
                "country": request.POST.get('country'),
                "landmark": request.POST.get('landmark'),
            }
        )

        # 2️⃣ Get all cart items
        cart_items = Cart_Page.objects.filter(user=user)
        if not cart_items.exists():
            return HttpResponse("Cart is empty")

        # 3️⃣ Create delivery for each cart item
        for item in cart_items:
            amount = item.cart_quantity * item.pro.selling_price  # make sure this matches your Cart_Page model
            dv, created = delivery.objects.get_or_create(
                user=user,
                cart=item,
                defaults={
                    "product":item.pro,
                    "shipping_address": ship,
                    "amount": amount
                }
            )
            if not created:
                dv.shipping_address = ship
                dv.amount = amount
                dv.save()

        # 4️⃣ Delete all cart items after deliveries created
        cart_items.delete()

        return redirect('order_page')

# class Delivery(View):
#     def get(self, request):
#         user = request.user

#         cart_items = Cart_Page.objects.filter(user=user)
#         ship = shipping.objects.filter(user=user).first()

#         if not cart_items.exists():
#             return HttpResponse("Cart is empty")

#         if not ship:
#             return HttpResponse("Add shipping first")

#         for item in cart_items:
#             # check if delivery already exists
#             dv, created = delivery.objects.get_or_create(
#                 user=user,
#                 cart=item,
#                 defaults={"shipping_address": ship},
#                 )
#             dv.amount=item.cart_quantity * item.pro.selling_price
#             dv.save()
#             item.delete()
#             # if already exists → update shipping
#             if not created:
#                 dv.shipping_address = ship
#                 dv.save()


#         return redirect('order_page')

class tracking_page(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        tracking=delivery.objects.filter(user=request.user)
        return render(request,'frontend/tracking_page.html',{'tracking':tracking})
        
class tracking_cancle(View):
    def get(self,request,id):
        delte_pro = get_object_or_404(delivery, id=id)
        delte_pro.delete()
        return redirect('tracking_page')
    
class search_View(View):
    def get(self,request):
        pro=Product.objects.filter(name=request.POST.get('search'))
        return render(request,'Base.html',{'pro':pro})

class Contact_Page_View(View):
    def get(self, request):
        return render(request, 'frontend/Contact_Page.html')

    def post(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to submit a support query.")
            return redirect('login')

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        query_type = request.POST.get('query_type')
        description = request.POST.get('description')
        
        # Format the feedback testimonial to fit the 238-character database field limit
        testimonial_text = description
        if len(testimonial_text) > 238:
            testimonial_text = testimonial_text[:235] + "..."

        FeedBack.objects.create(
            user=request.user,
            testimonial=testimonial_text,
            name=full_name,
            email=email,
            phone=phone,
            query_type=query_type
        )
        
        messages.success(
            request, 
            f"Thank you, {full_name}! Your ticket for '{query_type}' has been submitted successfully and saved under your feedback logs."
        )
        return redirect('contact')

class Searched_item(View):
    def get(self, request):
        from django.db.models import Q
        query = request.GET.get('search', '').strip()
        category_id = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort = request.GET.get('sort')

        products = Product.objects.filter(status=0)

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(vendor__icontains=query)
            )

        if category_id and category_id.isdigit():
            products = products.filter(category_id=int(category_id))

        if min_price and min_price.isdigit():
            products = products.filter(selling_price__gte=int(min_price))

        if max_price and max_price.isdigit():
            products = products.filter(selling_price__lte=int(max_price))

        if sort == 'low':
            products = products.order_by('selling_price')
        elif sort == 'high':
            products = products.order_by('-selling_price')
        elif sort == 'hot':
            products = products.filter(trending=True)

        categories = Category.objects.filter(status=0)

        if request.user.is_authenticated:
            liked_products = set(
                favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True)
            )
            no_fav = len(liked_products)
        else:
            liked_products = set()
            no_fav = 0

        context = {
            'pro': products,
            'categories': categories,
            'query': query,
            'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
            'liked_products': liked_products,
            'no_fav': no_fav,
            'total_results': products.count(),
        }
        return render(request, 'frontend/Searched_item_page.html', context)

    def post(self, request):
        from django.db.models import Q
        search = request.POST.get('search', '').strip()
        
        products = Product.objects.filter(status=0)
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
            
        categories = Category.objects.filter(status=0)
        
        if request.user.is_authenticated:
            liked_products = set(
                favourate.objects.filter(user=request.user).values_list('pro_duct_id', flat=True)
            )
            no_fav = len(liked_products)
        else:
            liked_products = set()
            no_fav = 0

        context = {
            'pro': products,
            'categories': categories,
            'query': search,
            'liked_products': liked_products,
            'no_fav': no_fav,
            'total_results': products.count(),
        }
        return render(request, 'frontend/Searched_item_page.html', context)
