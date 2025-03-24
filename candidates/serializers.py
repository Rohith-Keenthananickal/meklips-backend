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
    class Meta:
        model = CurrentAddress
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'street_address': {'help_text': 'Street address of the candidate'},
            'state': {'help_text': 'State of residence'},
            'city': {'help_text': 'City of residence'},
            'pincode': {'help_text': 'Postal/ZIP code'},
            'is_current_address': {'help_text': 'Whether this is the current address'}
        }

class EducationalDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalDegree
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'degree': {'help_text': 'Name of the degree'},
            'university': {'help_text': 'Name of the university'},
            'graduation_date': {'help_text': 'Date of graduation'},
            'graduation_month': {'help_text': 'Month of graduation'},
            'graduation_year': {'help_text': 'Year of graduation'},
            'location': {'help_text': 'Location of the university'},
            'field_of_study': {'help_text': 'Major or field of study'},
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
    class Meta:
        model = WorkExperience
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'designation': {'help_text': 'Job title or designation'},
            'company_name': {'help_text': 'Name of the company'},
            'start_date': {'help_text': 'Start date of employment'},
            'current_job': {'help_text': 'Whether this is the current job'},
            'end_date': {'help_text': 'End date of employment (if not current job)'},
            'responsibilities': {'help_text': 'Job responsibilities and achievements'},
            'contact_number': {'help_text': 'Contact number for reference'},
            'location': {'help_text': 'Location of employment'}
        }

class CandidateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSkill
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'skill_name': {'help_text': 'Name of the skill'},
            'skill_level': {'help_text': 'Proficiency level (1-5)'}
        }

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_address = CurrentAddressSerializer(read_only=True)
    educational_degrees = EducationalDegreeSerializer(many=True, read_only=True)
    social_media_links = SocialMediaLinkSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    candidate_skills = CandidateSkillSerializer(many=True, read_only=True)
    candidate_highlights = CandidateHighlightsSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ('user',)
        extra_kwargs = {
            'first_name': {'help_text': 'First name of the candidate'},
            'last_name': {'help_text': 'Last name of the candidate'},
            'phone': {'help_text': 'Primary phone number'},
            'mobile': {'help_text': 'Mobile phone number'},
            'dob': {'help_text': 'Date of birth'},
            'gender': {'help_text': 'Gender of the candidate'},
            'dp_id': {'help_text': 'Display picture ID'},
            'video_id': {'help_text': 'Video profile ID'},
            'experience_summary': {'help_text': 'Summary of work experience'},
            'technical_summary': {'help_text': 'Summary of technical skills'},
            'street_address': {'help_text': 'Current street address'}
        }

class CandidateSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'experience_summary', 'technical_summary')
        extra_kwargs = {
            'experience_summary': {'help_text': 'Summary of work experience'},
            'technical_summary': {'help_text': 'Summary of technical skills'}
        }

class CreateCandidateSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)  # Accept only userId from request

    # Allow nested writes for these fields
    current_address = CurrentAddressSerializer(write_only=True, required=False)
    educational_degrees = EducationalDegreeSerializer(many=True, write_only=True, required=False)
    social_media_links = SocialMediaLinkSerializer(many=True, write_only=True, required=False)
    work_experiences = WorkExperienceSerializer(many=True, write_only=True, required=False)
    candidate_skills = CandidateSkillSerializer(many=True, write_only=True, required=False)
    candidate_highlights = CandidateHighlightsSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Candidate
        fields = [
            'userId', 'first_name', 'last_name', 'phone', 'mobile', 'dob', 'gender', 
            'dp_id', 'video_id', 'experience_summary', 'technical_summary', 'street_address',
            'current_address', 'educational_degrees', 'social_media_links', 
            'work_experiences', 'candidate_skills', 'candidate_highlights'
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

        

