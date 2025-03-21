from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Candidate, CurrentAddress, EducationalDegree,
    SocialMediaLink, WorkExperience, CandidateSkill
)
from .serializers import (
    CandidateSerializer, CurrentAddressSerializer,
    EducationalDegreeSerializer, SocialMediaLinkSerializer,
    WorkExperienceSerializer, CandidateSkillSerializer,
    CandidateSummarySerializer
)

# Create your views here.

class CandidateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate profiles.
    
    Provides CRUD operations for candidate profiles and related data.
    """
    serializer_class = CandidateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Get the list of candidates for the current user.
        """
        return Candidate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new candidate profile for the current user.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_summary(self, request, pk=None):
        """
        Update the experience and technical summary of a candidate.
        
        Parameters:
            experience_summary (string): Updated experience summary
            technical_summary (string): Updated technical summary
        """
        candidate = self.get_object()
        serializer = CandidateSummarySerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentAddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate addresses.
    
    Provides CRUD operations for candidate addresses.
    """
    serializer_class = CurrentAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Get the list of addresses for the current user's candidate profile.
        """
        return CurrentAddress.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new address for the current user's candidate profile.
        """
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)

class EducationalDegreeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate educational degrees.
    
    Provides CRUD operations for candidate educational qualifications.
    """
    serializer_class = EducationalDegreeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Get the list of educational degrees for the current user's candidate profile.
        """
        return EducationalDegree.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new educational degree for the current user's candidate profile.
        """
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)

class SocialMediaLinkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate social media links.
    
    Provides CRUD operations for candidate social media profiles.
    """
    serializer_class = SocialMediaLinkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Get the list of social media links for the current user's candidate profile.
        """
        return SocialMediaLink.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new social media link for the current user's candidate profile.
        """
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)

class WorkExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate work experiences.
    
    Provides CRUD operations for candidate work history.
    """
    serializer_class = WorkExperienceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Get the list of work experiences for the current user's candidate profile.
        """
        return WorkExperience.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new work experience for the current user's candidate profile.
        """
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)

class CandidateSkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate skills.
    
    Provides CRUD operations for candidate skills and expertise.
    """
    serializer_class = CandidateSkillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Get the list of skills for the current user's candidate profile.
        """
        return CandidateSkill.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new skill for the current user's candidate profile.
        """
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)
