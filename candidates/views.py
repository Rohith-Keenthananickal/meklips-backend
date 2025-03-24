from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.custom_response import responseWrapper
from utils.decorators import swagger_response
from rest_framework.decorators import api_view
# from meklips.utils import api_view
from .models import (
    Candidate, CurrentAddress, EducationalDegree,
    SocialMediaLink, WorkExperience, CandidateSkill
)
from .serializers import (
    CandidateSerializer, CreateCandidateSerializer, CurrentAddressSerializer,
    EducationalDegreeSerializer, SocialMediaLinkSerializer,
    WorkExperienceSerializer, CandidateSkillSerializer,
    CandidateSummarySerializer
)

@swagger_response(request_serializer=CreateCandidateSerializer, response_serializer=CandidateSerializer, method='POST')
@api_view(['POST'])
def createCandidate(request):
    serializer = CreateCandidateSerializer(data=request.data)
    if serializer.is_valid():
        candidate = serializer.save()  # Save candidate
        candidate_serializer = CandidateSerializer(candidate)  # Serialize full candidate data
        return responseWrapper(True, candidate_serializer.data, "Candidate created successfully", 201)
    
    return responseWrapper(False, error=serializer.errors, message="Candidate creation failed", status_code=400)



@swagger_response(response_serializer=CandidateSerializer,method='GET')
@api_view(['GET'])
def getCandidateById(request, userId):
    try:
        candidate = Candidate.objects.get(user=userId)
        serializer = CandidateSerializer(candidate)
        return responseWrapper(True, serializer.data, "Candidate retrieved successfully", 200)
    except Candidate.DoesNotExist:
        return responseWrapper(False, None, "Candidate not found", 404)

# class CandidateView(APIView):
#     @swagger_response(response_serializer=CandidateSerializer)
#     def get(self, request, userId):
#         try:
#             candidate = Candidate.objects.get(user=userId)
#             serializer = CandidateSerializer(candidate)
#             return responseWrapper(True, serializer.data, "Candidate retrieved successfully", 200)
#         except Candidate.DoesNotExist:
#             return responseWrapper(False, None, "Candidate not found", 404)


#     @swagger_response(request_serializer=CandidateSerializer, response_serializer=CandidateSerializer)  # ✅ Request + Response
#     def post(self, request):
#         serializer = CandidateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return responseWrapper(True, serializer.data, "Candidate created successfully", 201)
#         return responseWrapper(False, serializer.errors, "Candidate creation failed", 400)

# class CandidateViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing candidate profiles.
    
#     Provides CRUD operations for candidate profiles and related data.
#     """
#     serializer_class = CandidateSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         """
#         Get the list of candidates for the current user.
#         """
#         return Candidate.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         """
#         Create a new candidate profile for the current user.
#         """
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['patch'])
#     def update_summary(self, request, pk=None):
#         """
#         Update the experience and technical summary of a candidate.
        
#         Parameters:
#             experience_summary (string): Updated experience summary
#             technical_summary (string): Updated technical summary
#         """
#         candidate = self.get_object()
#         serializer = CandidateSummarySerializer(candidate, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
