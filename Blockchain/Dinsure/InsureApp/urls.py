from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	       path('Register.html', views.Register, name="Register"),
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),	
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),
	       path('AddPolicy', views.AddPolicy, name="AddPolicy"),
	       path('AddPolicyAction', views.AddPolicyAction, name="AddPolicyAction"),
	       path('ViewPurchaseList', views.ViewPurchaseList, name="ViewPurchaseList"),
	       path('ViewClaimsRequest', views.ViewClaimsRequest, name="ViewClaimsRequest"),
	       path('ViewClaimsHistory', views.ViewClaimsHistory, name="ViewClaimsHistory"),
	       path('ViewPolicies', views.ViewPolicies, name="ViewPolicies"), 
	       path('GenerateClaim', views.GenerateClaim, name="GenerateClaim"), 	
	       path('ViewClaimStatus', views.ViewClaimStatus, name="ViewClaimStatus"),
	       path('ViewClaimsHistoryAction', views.ViewClaimsHistoryAction, name="ViewClaimsHistoryAction"),
	       path('ClaimRequestAction', views.ClaimRequestAction, name="ClaimRequestAction"), 	
	       path('ViewPolicyAction', views.ViewPolicyAction, name="ViewPolicyAction"), 
	       path('GenerateClaimAction', views.GenerateClaimAction, name="GenerateClaimAction"), 	
]
