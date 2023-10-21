from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Brand(models.Model):
    class Meta:
        verbose_name_plural = 'แบรนด์'
    name = models.CharField(max_length=50 , default="")
    desc = models.TextField(default="กรอกข้อมูลของแบรนด์สินค้า")
    def __str__(self):
        return self.name
    
class Product(models.Model):
    class Meta:
        verbose_name_plural = 'สินค้า'
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    amount = models.IntegerField()
    img1 = models.ImageField(blank=True, null=True)
    img2 = models.ImageField(blank=True, null=True)
    img3 = models.ImageField(blank=True, null=True)
    img4 = models.ImageField(blank=True, null=True)
    img5 = models.ImageField(blank=True, null=True)
    img6 = models.ImageField(blank=True, null=True)
    desc = models.TextField()
    code = models.CharField(max_length=200,blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    published = models.BooleanField(default=True)
    def show_image(self):
        if self.img1:
            return format_html('<img src="'+ self.img1.url+'" height=70px>')
        return ''
    show_image.allow_tags = True
    show_image.short_description = 'Image'
    @property
    def imageURL(self):
        try:
          url = self.img1.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return str(self.id) + " : " + self.name
    
    def get_comment_count(self):
        return self.productcomment_set.count()
    
class ProductComment(models.Model):
    class Meta:
        verbose_name_plural = 'คอมเม้นต์สินค้า'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(default="Comment.....")
    rating = models.FloatField()
    created = models.DateTimeField(auto_now_add=False)
    updated = models.DateTimeField(auto_now_add=False)
    def __str__(self):
        return self.comment
    
class Size(models.Model):
    class Meta:
        verbose_name_plural = 'ไซส์รองเท้า'
    size = models.CharField(max_length=10)
    
    def __str__(self):
        return str(self.id) + " : " + self.size
    
class Customer(models.Model):
    class Meta:
        verbose_name_plural = 'ผู้ใช้งาน'
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    def __str__(self):
        return str(self.id) + " : " + self.name



class Order(models.Model):
    class Meta:
        verbose_name_plural = 'ออเดอร์'
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product:
                shipping = True
            return shipping
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
    
class OrderItem(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    country = models.CharField(default="Thailand",max_length=200,blank=True,null=True)
    city = models.CharField(max_length=200,blank=True,null=True)
    state = models.CharField(max_length=200,blank=True,null=True)
    zipcode = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(default="+66",max_length=17,blank=True,null=True)
    def __str__(self):
        return str(self.address)
    