from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

class traveltype(models.Model):
    traveltype_id = models.AutoField(primary_key=True)
    traveltypedescription = models.CharField(max_length=40, null=False)

    class Meta:
        managed = True
        db_table = 'traveltype'  

    def __str__(self):
        return self.traveltypedescription

class travelplan(models.Model):
    travelplan_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50, null=False)
    territory = models.CharField(max_length=100, null=False)
    datestart = models.DateTimeField(null=False)
    datefinish = models.DateTimeField(null=False)
    quantitydays = models.IntegerField(null=False)
    description = models.CharField(max_length=1000)
    traveltype = models.ForeignKey('traveltype', on_delete=models.CASCADE, null=False)    
    image = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey('user.user', on_delete=models.CASCADE, null=False)
    is_public = models.BooleanField(default=False)
    friends_only = models.BooleanField(default=False)
    total_distance_travelled = models.FloatField(null=True, blank=True)
    total_time_seconds = models.IntegerField(null=True, blank=True)
    moving_time_seconds = models.IntegerField(null=True, blank=True)
    speed_midle = models.FloatField(null=True, blank=True)
    speed_moving = models.FloatField(null=True, blank=True)
    total_ascent = models.FloatField(null=True, blank=True)
    total_descent = models.FloatField(null=True, blank=True)
    travelplan_geo = models.ForeignKey('travelplan_geo', on_delete=models.CASCADE, null=False)

    class Meta:
        managed = True
        db_table = 'travelplan'

    def __str__(self):
        # Возвращает строковое представление объекта, используя правильное имя поля ForeignKey.
        return f"Travel Plan {self.travelplan_id} - {self.traveltype}"  

class travelplan_geo(models.Model):
    travelplan_geo_id = models.AutoField(primary_key=True)    
    gpxtrek  = models.TextField(null=True)
    graph_data = models.JSONField(null=True, blank=True)
    geojson = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"TravelPlanGeo {self.travelplan_geo_id}"

    def save_graph_data(self, data):
        """Сохранение сериализованных данных графика."""
        self.graph_data = data
        self.save()

    def get_graph_data(self):
        """Извлечение данных графика."""
        return self.graph_data

class booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    namebooking = models.CharField(max_length=60, null=False)
    datestart = models.DateTimeField(null=False)
    datefinish = models.DateTimeField(null=False)
    adress = models.CharField(max_length=200) 

    class Meta:
        managed = True
        db_table = 'booking' 
    
    def __str__(self):
        return f"Booking {self.booking_id}"
    
class expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    typeexpense = models.CharField(max_length=30, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    currency = models.CharField(max_length=30, null=False)    

    class Meta:
        managed = True
        db_table = 'expense' 
    
    def __str__(self):
        return f"Expense {self.expense_id}"
    
class sight(models.Model):
    sight_id = models.AutoField(primary_key=True)
    coordinates = models.PointField(geography=True, null=False)
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    
    class Meta:
        managed = True
        db_table = 'sight' 
    
    def __str__(self):
        return f"Expense {self.sight_id}"
    
class ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    typeticket = models.CharField(max_length=40)
    datestart = models.DateTimeField(null=False)
    datefinish = models.DateTimeField(null=False)
    adressstart = models.CharField(max_length=200)   

    class Meta:
        managed = True
        db_table = 'ticket' 
    
    def __str__(self):
        return f"Expense {self.sight_id}"
    
class point_trek(models.Model):
    point_trek_id = models.AutoField(primary_key=True)
    namepoint = models.CharField(max_length=40)
    description = models.CharField(max_length=400)
    point_сoordinates = models.JSONField(null=True, blank=True)    

    class Meta:
        managed = True
        db_table = 'point_trek' 
    
    def __str__(self):
        return f"Point {self.point_trek_id}"

class plpoint_trek(models.Model):
    travelplan = models.ForeignKey('travelplan', on_delete=models.CASCADE)
    point_trek = models.ForeignKey('point_trek', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('travelplan', 'point_trek')

    def __str__(self):
        return f"Travel Plan Sight ({self.travelplan.travelplan_id}, {self.point_trek.point_trek_id})"

    
class Friendship(models.Model):
    user1 = models.ForeignKey('user.user', on_delete=models.CASCADE, related_name="friendships1")
    user2 = models.ForeignKey('user.user', on_delete=models.CASCADE, related_name="friendships2")

#Дальше идут таблицы многие ко многим

class travelplansight(models.Model):
    travelplan = models.ForeignKey('travelplan', on_delete=models.CASCADE)
    sight = models.ForeignKey('sight', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('travelplan', 'sight')

    def __str__(self):
        return f"Travel Plan Sight ({self.travelplan.travelplan_id}, {self.sight.sight_id})"


class travelplanexpense(models.Model):
    travelplan = models.ForeignKey('travelplan', on_delete=models.CASCADE)
    expense = models.ForeignKey('expense', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('travelplan', 'expense')

    def __str__(self):
        return f"Travel Plan Expense ({self.travelplan.travelplan_id}, {self.expense.expense_id})"


class travelplanticket(models.Model):
    travelplan = models.ForeignKey('travelplan', on_delete=models.CASCADE)
    ticket = models.ForeignKey('ticket', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('travelplan', 'ticket')

    def __str__(self):
        return f"Travel Plan Ticket ({self.travelplan.travelplan_id}, {self.ticket.ticket_id})"
    
class travelplanbooking(models.Model):
    travelplan = models.ForeignKey('travelplan', on_delete=models.CASCADE)
    booking = models.ForeignKey('booking', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('travelplan', 'booking')

    def __str__(self):
        return f"Travel Plan Booking ({self.travelplan.travelplan_id}, {self.booking.booking_id})"