from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from .models import (
    Candidate, CurrentAddress, EducationalDegree,
    SocialMediaLink, WorkExperience, CandidateSkill, CandidateHighlights
)

User = get_user_model()

class CandidateHighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateHighlights
        fields = '__all__'
        read_only_fields = ('candidate',)   



class CurrentAddressSerializer(serializers.ModelSerializer):
    streetAddress = serializers.CharField(source='street_address')
    isCurrentAddress = serializers.BooleanField(source='is_current_address')

    class Meta:
        model = CurrentAddress
        fields = ['id', 'streetAddress', 'state', 'city', 'pincode', 'isCurrentAddress']
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'streetAddress': {'help_text': 'Street address of the candidate'},
            'state': {'help_text': 'State of residence'},
            'city': {'help_text': 'City of residence'},
            'pincode': {'help_text': 'Postal/ZIP code'},
            'isCurrentAddress': {'help_text': 'Whether this is the current address'}
        }

class EducationalDegreeSerializer(serializers.ModelSerializer):
    graduationDate = serializers.DateField(source='graduation_date')
    graduationMonth = serializers.CharField(source='graduation_month')
    graduationYear = serializers.IntegerField(source='graduation_year')
    fieldOfStudy = serializers.CharField(source='field_of_study')

    class Meta:
        model = EducationalDegree
        fields = ['id', 'degree', 'university', 'graduationDate', 'graduationMonth', 
                 'graduationYear', 'location', 'fieldOfStudy', 'notes']
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'degree': {'help_text': 'Name of the degree'},
            'university': {'help_text': 'Name of the university'},
            'graduationDate': {'help_text': 'Date of graduation'},
            'graduationMonth': {'help_text': 'Month of graduation'},
            'graduationYear': {'help_text': 'Year of graduation'},
            'location': {'help_text': 'Location of the university'},
            'fieldOfStudy': {'help_text': 'Major or field of study'},
            'notes': {'help_text': 'Additional notes about the degree'}
        }

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'type': {'help_text': 'Type of social media (e.g., LinkedIn, GitHub)'},
            'url': {'help_text': 'URL of the social media profile'}
        }

class WorkExperienceSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='company_name')
    currentJob = serializers.BooleanField(source='current_job',required=False)
    startDate = serializers.DateField(source='start_date',required=False)
    endDate = serializers.DateField(source='end_date',required=False)
    contactNumber = serializers.CharField(source='contact_number',required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = WorkExperience
        fields = ['id', 'designation', 'companyName', 'currentJob', 'startDate', 
                 'endDate', 'responsibilities', 'contactNumber', 'location']
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'designation': {'help_text': 'Job title or designation'},
            'companyName': {'help_text': 'Name of the company'},
            'startDate': {'help_text': 'Start date of employment'},
            'currentJob': {'help_text': 'Whether this is the current job'},
            'endDate': {'help_text': 'End date of employment (if not current job)'},
            'responsibilities': {'help_text': 'Job responsibilities and achievements'},
            'contactNumber': {'help_text': 'Contact number for reference'},
            'location': {'help_text': 'Location of employment'}
        }

class CandidateSkillSerializer(serializers.ModelSerializer):
    skillName = serializers.CharField(source='skill_name')
    skillLevel = serializers.IntegerField(source='skill_level')

    class Meta:
        model = CandidateSkill
        fields = ['id', 'skillName', 'skillLevel']
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'skillName': {'help_text': 'Name of the skill'},
            'skillLevel': {'help_text': 'Proficiency level (1-5)'}
        }

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    currentAddress = CurrentAddressSerializer(source='current_address', read_only=True)
    educationalDegrees = EducationalDegreeSerializer(source='educational_degrees', many=True, read_only=True)
    socialMediaLinks = SocialMediaLinkSerializer(source='social_media_links', many=True, read_only=True)
    workExperiences = WorkExperienceSerializer(source='work_experiences', many=True, read_only=True)
    candidateSkills = CandidateSkillSerializer(source='candidate_skills', many=True, read_only=True)
    candidateHighlights = CandidateHighlightsSerializer(source='candidate_highlights', many=True, read_only=True)
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    experienceSummary = serializers.CharField(source='experience_summary')
    technicalSummary = serializers.CharField(source='technical_summary')
    streetAddress = serializers.CharField(source='street_address')
    dpId = serializers.CharField(source='dp_id')
    videoId = serializers.CharField(source='video_id')

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'firstName', 'lastName', 'phone', 'mobile', 'dob', 'gender',
                 'dpId', 'videoId', 'experienceSummary', 'technicalSummary', 'streetAddress',
                 'currentAddress', 'educationalDegrees', 'socialMediaLinks',
                 'workExperiences', 'candidateSkills', 'candidateHighlights']
        read_only_fields = ('user',)
        extra_kwargs = {
            'firstName': {'help_text': 'First name of the candidate'},
            'lastName': {'help_text': 'Last name of the candidate'},
            'phone': {'help_text': 'Primary phone number'},
            'mobile': {'help_text': 'Mobile phone number'},
            'dob': {'help_text': 'Date of birth'},
            'gender': {'help_text': 'Gender of the candidate'},
            'dpId': {'help_text': 'Display picture ID'},
            'videoId': {'help_text': 'Video profile ID'},
            'experienceSummary': {'help_text': 'Summary of work experience'},
            'technicalSummary': {'help_text': 'Summary of technical skills'},
            'streetAddress': {'help_text': 'Current street address'}
        }

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary, excluding null values.
        """
        representation = super().to_representation(instance)
        # Remove null values from the representation
        return {k: v for k, v in representation.items() if v is not None}

class CandidateSummarySerializer(serializers.ModelSerializer):
    experienceSummary = serializers.CharField(source='experience_summary')
    technicalSummary = serializers.CharField(source='technical_summary')

    class Meta:
        model = Candidate
        fields = ['id', 'experienceSummary', 'technicalSummary']
        extra_kwargs = {
            'experienceSummary': {'help_text': 'Summary of work experience'},
            'technicalSummary': {'help_text': 'Summary of technical skills'}
        }

class CreateCandidateSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)
    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)
    experienceSummary = serializers.CharField(source='experience_summary', required=False)
    technicalSummary = serializers.CharField(source='technical_summary', required=False)
    streetAddress = serializers.CharField(source='street_address', required=False)
    dpId = serializers.CharField(source='dp_id', required=False)
    videoId = serializers.CharField(source='video_id', required=False)
    phone = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    dob = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)

    # Allow nested writes for these fields
    currentAddress = CurrentAddressSerializer(source='current_address', write_only=True, required=False)
    educationalDegrees = EducationalDegreeSerializer(source='educational_degrees', many=True, write_only=True, required=False)
    socialMediaLinks = SocialMediaLinkSerializer(source='social_media_links', many=True, write_only=True, required=False)
    workExperiences = WorkExperienceSerializer(source='work_experiences', many=True, write_only=True, required=False)
    candidateSkills = CandidateSkillSerializer(source='candidate_skills', many=True, write_only=True, required=False)
    candidateHighlights = CandidateHighlightsSerializer(source='candidate_highlights', many=True, write_only=True, required=False)

    class Meta:
        model = Candidate
        fields = [
            'userId', 'firstName', 'lastName', 'phone', 'mobile', 'dob', 'gender', 
            'dpId', 'videoId', 'experienceSummary', 'technicalSummary', 'streetAddress',
            'currentAddress', 'educationalDegrees', 'socialMediaLinks', 
            'workExperiences', 'candidateSkills', 'candidateHighlights'
        ]

    def validate_userId(self, value):
        try:
            user = User.objects.get(id=value)
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            
            # Check if user already has a candidate profile
            if hasattr(user, 'candidate_profile'):
                raise serializers.ValidationError("User already has a candidate profile")
                
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with ID {value} does not exist")

    def create(self, validated_data):
        user_id = validated_data.pop('userId')

        # Fetch user object using userId
        try:
            user = User.objects.get(id=user_id)
            
            # Check if user already has a candidate profile
            if hasattr(user, 'candidate_profile'):
                raise serializers.ValidationError("User already has a candidate profile")
                
        except User.DoesNotExist:
            raise serializers.ValidationError({"userId": f"User with ID {user_id} not found"})

        # Extract nested data
        current_address = validated_data.pop('current_address', None)
        educational_degrees = validated_data.pop('educational_degrees', [])
        social_media_links = validated_data.pop('social_media_links', [])
        work_experiences = validated_data.pop('work_experiences', [])
        candidate_skills = validated_data.pop('candidate_skills', [])
        candidate_highlights = validated_data.pop('candidate_highlights', [])

        # Create Candidate object with user object directly
        try:
            candidate = Candidate.objects.create(user=user, **validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

        # Handle nested fields if provided
        if current_address:
            CurrentAddress.objects.create(candidate=candidate, **current_address)
        if educational_degrees:
            for edu_data in educational_degrees:
                EducationalDegree.objects.create(candidate=candidate, **edu_data)
        if social_media_links:
            for social_data in social_media_links:
                SocialMediaLink.objects.create(candidate=candidate, **social_data)
        if work_experiences:
            for work_data in work_experiences:
                WorkExperience.objects.create(candidate=candidate, **work_data)
        if candidate_skills:
            for skill_data in candidate_skills:
                CandidateSkill.objects.create(candidate=candidate, **skill_data)
        if candidate_highlights:
            for highlight_data in candidate_highlights:
                CandidateHighlights.objects.create(candidate=candidate, **highlight_data)

        return candidate

        

