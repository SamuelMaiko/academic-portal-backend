from rest_framework import serializers
from a_userauth.models import CustomUser

class UsersAnalyticsSerializer(serializers.ModelSerializer):
    full_name= serializers.SerializerMethodField()
    assigned_work= serializers.SerializerMethodField()
    uptaken_work= serializers.SerializerMethodField()
    poor_work= serializers.SerializerMethodField()
    average_score= serializers.SerializerMethodField()

    class Meta:
        model=CustomUser
        fields=['id', 'registration_number','full_name','assigned_work', 'uptaken_work', 'poor_work', 'average_score']

    def get_full_name(self, obj):
        return obj.first_name +" "+obj.last_name

    def get_assigned_work(self, obj):
        return obj.assigned_work.count()
    
    def get_uptaken_work(self, obj):
        return obj.uptaken_work.count()
    def get_poor_work(self, obj):
        return obj.default_work.filter(type="QualityIssues").count()
    
    def get_average_score(self, obj):
        total_work = self.get_assigned_work(obj) + self.get_uptaken_work(obj)
        
        if total_work == 0:
            return 100.0  

        poor_work = self.get_poor_work(obj)
        return 100.0 - (poor_work / total_work) * 100.0