from django.contrib import admin

# Register your models here.

from app02.models import User,Passenger,Flight,Airport,Order

class UserAdmin(admin.ModelAdmin):
    fields = ['userid','name','idnum','telnum','email']
    list_display = ('userid','name','idnum','telnum','email')
    search_fields = ('userid','name','idnum','telnum')
    list_per_page = 50

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name','idnum','telnum')
    list_per_page = 50
    search_fields = ('name','idnum','telnum')

class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_id','departure_day','departure_time','company')
    list_per_page = 50
    search_fields = ('flight_id','departure_day','company')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','flightnum','departure_day','ordertime')
    list_per_page = 50
    search_fields = ('id','flightnum','departure_day')

class AirportAdmin(admin.ModelAdmin):
    list_display = ('airport_id','airport_name','city')
    list_per_page = 50
    search_fields = ('airport_id','airport_name','city')


admin.site.register(User,UserAdmin)
admin.site.register(Passenger,PassengerAdmin)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Airport,AirportAdmin)

