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
        extra_kwargs = {
            'highlightkey': {'help_text': 'Key of the highlight'},
            'highlightValue': {'help_text': 'Value of the highlight'}
        }

class CurrentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAddress
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'streetAddress': {'help_text': 'Street address of the candidate'},
            'state': {'help_text': 'State of residence'},
            'city': {'help_text': 'City of residence'},
            'pincode': {'help_text': 'Postal/ZIP code'},
            'isCurrentAddress': {'help_text': 'Whether this is the current address'}
        }

class EducationalDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalDegree
        fields = '__all__'
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
    class Meta:
        model = WorkExperience
        fields = '__all__'
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
    class Meta:
        model = CandidateSkill
        fields = '__all__'
        read_only_fields = ('candidate',)
        extra_kwargs = {
            'skillName': {'help_text': 'Name of the skill'},
            'skillLevel': {'help_text': 'Proficiency level (1-5)'}
        }

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    currentAddress = CurrentAddressSerializer(read_only=True)
    educationalDegrees = EducationalDegreeSerializer(many=True, read_only=True)
    socialMediaLinks = SocialMediaLinkSerializer(many=True, read_only=True)
    workExperiences = WorkExperienceSerializer(many=True, read_only=True)
    candidateSkills = CandidateSkillSerializer(many=True, read_only=True)
    candidateHighlights = CandidateHighlightsSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
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
            'streetAddress': {'help_text': 'Current street address'},
            'zipCode': {'help_text': 'Zip code of the current address'},
            'professionInfo': {'help_text': 'Profession information'},
            'state': {'help_text': 'State of residence'},
            'city': {'help_text': 'City of residence'},
            'streetAddress2': {'help_text': 'Secondary street address'},
            'professionInfo': {'help_text': 'Profession information'},
        }

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary, excluding null values.
        """
        representation = super().to_representation(instance)
        # Remove null values from the representation
        return {k: v for k, v in representation.items() if v is not None}

class CandidateSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'experienceSummary', 'technicalSummary')
        extra_kwargs = {
            'experienceSummary': {'help_text': 'Summary of work experience'},
            'technicalSummary': {'help_text': 'Summary of technical skills'}
        }

class CreateCandidateSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)
    
    # Allow nested writes for these fields
    currentAddress = CurrentAddressSerializer(write_only=True, required=False)
    educationalDegrees = EducationalDegreeSerializer(many=True, write_only=True, required=False)
    socialMediaLinks = SocialMediaLinkSerializer(many=True, write_only=True, required=False)
    workExperiences = WorkExperienceSerializer(many=True, write_only=True, required=False)
    candidateSkills = CandidateSkillSerializer(many=True, write_only=True, required=False)
    candidateHighlights = CandidateHighlightsSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Candidate
        fields = [
            'userId', 'firstName', 'lastName', 'phone', 'mobile', 'dob', 'gender', 
            'dpId', 'videoId', 'experienceSummary', 'technicalSummary',
            'currentAddress', 'educationalDegrees', 'socialMediaLinks', 
            'workExperiences', 'candidateSkills', 'candidateHighlights', 'professionInfo',
            'state', 'city', 'streetAddress2', 'streetAddress', 'zipCode'
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
        current_address = validated_data.pop('currentAddress', None)
        educational_degrees = validated_data.pop('educationalDegrees', [])
        social_media_links = validated_data.pop('socialMediaLinks', [])
        work_experiences = validated_data.pop('workExperiences', [])
        candidate_skills = validated_data.pop('candidateSkills', [])
        candidate_highlights = validated_data.pop('candidateHighlights', [])

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

        

