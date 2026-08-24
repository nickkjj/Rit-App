from django.db.models import F, Q, CheckConstraint, UniqueConstraint
from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=150)
    position_name = models.CharField(max_length=100)

    is_authenticated = models.BooleanField(default=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.name}"

class LeaderLead(models.Model):
    leader = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leads")
    lead = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaders")

    class Meta:
        db_table = 'leader_lead'

        constraints = [
            UniqueConstraint(
                fields=['leader', 'lead'],
                name='unique_leader_lead_pk'
            ),

            CheckConstraint(
                condition=~Q(leader=F('lead')), 
                name='chk_no_self_lead'
            )
        ]

        def __str__(self):
            return f"{self.leader.name} leads {self.lead.name}"


    
