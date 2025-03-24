from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20,null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    dp_id = models.TextField(null=True, blank=True)
    video_id = models.TextField(null=True, blank=True)
    experience_summary = models.TextField(null=True, blank=True)
    technical_summary = models.TextField(null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Candidate(id={self.id}, user={self.user.username}, name={self.first_name} {self.last_name})"

    class Meta:
        db_table = 'TBL_CANDIDATE'

class CurrentAddress(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name='current_address')
    street_address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_current_address = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.candidate.first_name}'s Address"
    
    class Meta:
        db_table = 'TBL_CURRENT_ADDRESS'

class EducationalDegree(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educational_degrees')
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=200)
    graduation_date = models.DateField()
    graduation_month = models.CharField(max_length=20)
    graduation_year = models.IntegerField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    field_of_study = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.degree} from {self.university}"
    
    class Meta:
        db_table = 'TBL_EDUCATIONAL_DEGREE'

class SocialMediaLink(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='social_media_links')
    type = models.CharField(max_length=50)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.first_name}'s {self.type}"
    
    class Meta:
        db_table = 'TBL_SOCIAL_MEDIA_LINK'

class WorkExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='work_experiences')
    designation = models.CharField(max_length=100,null=True, blank=True)
    company_name = models.CharField(max_length=200,null=True, blank=True)
    start_date = models.DateField(null=True, blank=True )
    current_job = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20,null=True, blank=True)
    location = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.designation} at {self.company_name}"

    class Meta:
        db_table = 'TBL_WORK_EXPERIENCE'

class CandidateSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_skills')
    skill_name = models.CharField(max_length=100)
    skill_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.first_name}'s {self.skill_name}"
    
    class Meta:
        db_table = 'TBL_CANDIDATE_SKILL'


class CandidateHighlights(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_highlights')
    highlightkey = models.TextField()
    highlightvalue = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.candidate.first_name}'s {self.highlightkey}"
    
    class Meta:
        db_table = 'TBL_CANDIDATE_HIGHLIGHTS'


