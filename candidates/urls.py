from django.urls import path, include
from rest_framework.routers import DefaultRouter

from candidates import views as candidate_views
# from .views import (
#     CandidateView, CandidateViewSet, CurrentAddressViewSet,
#     EducationalDegreeViewSet, SocialMediaLinkViewSet,
#     WorkExperienceViewSet, CandidateSkillViewSet
# )

router = DefaultRouter()
# router.register(r'candidates', CandidateViewSet, basename='candidate')
# router.register(r'current-addresses', CurrentAddressViewSet, basename='current-address')
# router.register(r'educational-degrees', EducationalDegreeViewSet, basename='educational-degree')
# router.register(r'social-media-links', SocialMediaLinkViewSet, basename='social-media-link')
# router.register(r'work-experiences', WorkExperienceViewSet, basename='work-experience')
# router.register(r'candidate-skills', CandidateSkillViewSet, basename='candidate-skill')

urlpatterns = [
    path('', candidate_views.createCandidate, name='candidate-list'),  # For POST
    path('<int:userId>', candidate_views.getCandidateById, name='candidate-detail'),  # For GET
]