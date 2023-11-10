from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	   
	       path('OwnerLogin', views.OwnerLogin, name="OwnerLogin"),
	       path('OwnerLoginAction', views.OwnerLoginAction, name="OwnerLoginAction"),	
	       path('Signup', views.Signup, name="Signup"),
	       path('SignupAction', views.SignupAction, name="SignupAction"),
	       path('AddCars', views.AddCars, name="AddCars"),
	       path('AddCarsAction', views.AddCarsAction, name="AddCarsAction"),
	       path('ViewBookedHistory', views.ViewBookedHistory, name="ViewBookedHistory"),
	       path('BookCars', views.BookCars, name="BookCars"),
	       path('BookCarsAction', views.BookCarsAction, name="BookCarsAction"),
	       path('PaymentAction', views.PaymentAction, name="PaymentAction"),
	       path('ViewHistory', views.ViewHistory, name="ViewHistory"),
	       path('ReleasedBookCars', views.ReleasedBookCars, name="ReleasedBookCars"),
	       path('ReleasedBookCarsAction', views.ReleasedBookCarsAction, name="ReleasedBookCarsAction"),
]
