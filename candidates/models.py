from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    firstName = models.CharField(max_length=100, db_column='first_name')
    lastName = models.CharField(max_length=100, db_column='last_name')
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dpId = models.TextField(null=True, blank=True, db_column='dp_id')
    videoId = models.TextField(null=True, blank=True, db_column='video_id')
    experienceSummary = models.TextField(null=True, blank=True, db_column='experience_summary')
    technicalSummary = models.TextField(null=True, blank=True, db_column='technical_summary')
    professionInfo = models.TextField(null=True, blank=True, db_column='profession_info')
    streetAddress = models.CharField(max_length=255, null=True, blank=True, db_column='street_address')
    streetAddress2 = models.CharField(max_length=255, null=True, blank=True, db_column='street_address2')
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zipCode = models.CharField(max_length=20, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    def __str__(self):
        return f"Candidate(id={self.id}, user={self.user.username}, name={self.firstName} {self.lastName})"

    class Meta:
        db_table = 'TBL_CANDIDATE'

class CurrentAddress(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name='currentAddress')
    streetAddress = models.CharField(max_length=255, db_column='street_address',null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    pincode = models.CharField(max_length=10,null=True, blank=True)
    isCurrentAddress = models.BooleanField(default=True, db_column='is_current_address',null=True, blank=True)

    def __str__(self):
        return f"{self.candidate.firstName}'s Address"
    
    class Meta:
        db_table = 'TBL_CURRENT_ADDRESS'

class EducationalDegree(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educationalDegrees')
    degree = models.CharField(max_length=100,null=True, blank=True)
    university = models.CharField(max_length=200,null=True, blank=True)
    graduationDate = models.DateField(db_column='graduation_date',null=True, blank=True)
    graduationMonth = models.CharField(max_length=20, db_column='graduation_month',null=True, blank=True)
    graduationYear = models.IntegerField(db_column='graduation_year',null=True, blank=True)
    location = models.CharField(max_length=200,null=True, blank=True)
    notes = models.TextField(blank=True,null=True)
    fieldOfStudy = models.CharField(max_length=200, db_column='field_of_study',null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    def __str__(self):
        return f"{self.degree} from {self.university}"
    
    class Meta:
        db_table = 'TBL_EDUCATIONAL_DEGREE'

class SocialMediaLink(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='socialMediaLinks')
    type = models.CharField(max_length=50,null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    def __str__(self):
        return f"{self.candidate.firstName}'s {self.type}"
    
    class Meta:
        db_table = 'TBL_SOCIAL_MEDIA_LINK'

class WorkExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='workExperiences')
    designation = models.CharField(max_length=100, null=True, blank=True)
    companyName = models.CharField(max_length=200, null=True, blank=True, db_column='company_name')
    startDate = models.DateField(null=True, blank=True, db_column='start_date')
    currentJob = models.BooleanField(default=False, db_column='current_job',null=True, blank=True)
    endDate = models.DateField(null=True, blank=True, db_column='end_date')
    responsibilities = models.TextField(null=True, blank=True)
    contactNumber = models.CharField(max_length=20, null=True, blank=True, db_column='contact_number')
    location = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    def __str__(self):
        return f"{self.designation} at {self.companyName}"

    class Meta:
        db_table = 'TBL_WORK_EXPERIENCE'

class CandidateSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidateSkills')
    skillName = models.CharField(max_length=100, db_column='skill_name',null=True, blank=True)
    skillLevel = models.IntegerField(db_column='skill_level',null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    def __str__(self):
        return f"{self.candidate.firstName}'s {self.skillName}"
    
    class Meta:
        db_table = 'TBL_CANDIDATE_SKILL'

class CandidateHighlights(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidateHighlights')
    highlightKey = models.TextField(db_column='highlightkey',null=True, blank=True)
    highlightValue = models.TextField(db_column='highlightvalue',null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')
    
    def __str__(self):
        return f"{self.candidate.firstName}'s {self.highlightKey}"
    
    class Meta:
        db_table = 'TBL_CANDIDATE_HIGHLIGHTS'


