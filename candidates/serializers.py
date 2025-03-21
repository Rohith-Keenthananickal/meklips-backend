from rest_framework import serializers
from users.serializers import UserSerializer
from .models import (
    Candidate, CurrentAddress, EducationalDegree,
    SocialMediaLink, WorkExperience, CandidateSkill
)

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