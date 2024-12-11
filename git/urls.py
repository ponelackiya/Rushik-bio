from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import update_cart_quantity

app_name='blog'

urlpatterns=[
    path('',views.home,name='home'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_page,name='login'),
    path('offers/',views.offer_view,name='offers'),
    path('logout/',views.logout_page,name='logout'),
    path("category/", views.category, name="category"),
    path('profile/', views.profile, name='profile'),
    path("view_category/<str:name>/", views.view_category, name="view_category"),
    path("product_detail/<str:cname>/<str:pname>", views.product_detail, name="product_detail"),
    path('addtocart/',views.add_to_cart,name='addtocart'),
    path('cart/',views.cart_page,name='cart'),
    path('fav/',views.fav_page,name='fav'),
    path('favview/',views.favview,name='favview'),
    path("delet_cart/<str:cid>",views.delet_cart,name='delet_cart'),
    path("delet_fav/<str:fid>",views.delet_fav,name='delet_fav'),
    path('search/', views.search_results, name='search'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('address/',views.address_view, name='address'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/', views.order_view, name='order_view'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('delete-order-item/<int:item_id>/', views.delete_order_item, name='delete_order_item'),
    path('update-cart-quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('cash-page/', views.cash_page_view, name='cash_page'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('cash/', views.cash_view, name='cash'),
    path('refund/', views.refund_view, name='refund'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('shipping/', views.shipping_view, name='shipping'),
    path("get_otp/", views.get_otp_view, name="get_otp"),
    path("verify_otp/", views.verify_otp_view, name="verify_otp"),
    path("reset_password/", views.reset_password_view, name="reset_password"),

    # path('payment_page/', views.pay_view, name='payment_page'),  # Route for the payment page

    path('payment/', views.payment_view, name='payment_view'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    # path('cart/<int:total_amount>/', views.cart_view, name='cart_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
