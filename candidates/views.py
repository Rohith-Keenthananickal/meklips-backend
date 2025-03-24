from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.custom_response import responseWrapper
from utils.decorators import swagger_response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
# from meklips.utils import api_view
from .models import (
    Candidate, CurrentAddress, EducationalDegree,
    SocialMediaLink, WorkExperience, CandidateSkill, CandidateHighlights
)
from .serializers import (
    CandidateSerializer, CreateCandidateSerializer, CurrentAddressSerializer,
    EducationalDegreeSerializer, SocialMediaLinkSerializer,
    WorkExperienceSerializer, CandidateSkillSerializer,
    CandidateSummarySerializer
)
from django.db import transaction
import os
from django.conf import settings

@swagger_response(request_serializer=CreateCandidateSerializer, response_serializer=CandidateSerializer, method='POST')
@api_view(['POST'])
def createCandidate(request):
    serializer = CreateCandidateSerializer(data=request.data)
    if serializer.is_valid():
        candidate = serializer.save()  # Save candidate
        candidate_serializer = CandidateSerializer(candidate)  # Serialize full candidate data
        return responseWrapper(True, candidate_serializer.data, "Candidate created successfully", 201)
    
    return responseWrapper(False, error=serializer.errors, message="Candidate creation failed", status_code=400)



class CandidateDetailView(APIView):
    @swagger_auto_schema(
        responses={200: CandidateSerializer(), 404: "Candidate not found"},
    )
    def get(self, request, userId):
        """Retrieve a candidate by userId."""
        try:
            candidate = Candidate.objects.get(user_id=userId)
            serializer = CandidateSerializer(candidate)
            return responseWrapper(True, serializer.data, "Candidate retrieved successfully", 200)
        except Candidate.DoesNotExist:
            return responseWrapper(False, None, "Candidate not found", 404)

    @swagger_auto_schema(
        responses={200: "Candidate deleted successfully", 404: "Candidate not found"},
    )
    def delete(self, request, userId):
        try:
            candidate = Candidate.objects.get(user_id=userId)
            candidate.delete()
            return responseWrapper(True, None, "Candidate deleted successfully", 200)
        except Candidate.DoesNotExist:
            return responseWrapper(False, None, "Candidate not found", 404)
        
    @swagger_auto_schema(
        request_body=CandidateSerializer,
        responses={200: "Candidate updated successfully", 404: "Candidate not found"},
    )
    def put(self, request, userId):
        try:
            candidate = Candidate.objects.get(user_id=userId)
            serializer = CandidateSerializer(candidate, data=request.data, partial=True)

            if serializer.is_valid():
                with transaction.atomic():  # Ensures all updates succeed or roll back
                    serializer.save()

                    # Update related objects dynamically
                    related_models = {
                        "current_address": CurrentAddress,
                        "work_experiences": WorkExperience,
                        "educational_degrees": EducationalDegree,
                        "social_media_links": SocialMediaLink,
                        "candidate_skills": CandidateSkill,
                        "candidate_highlights": CandidateHighlights
                    }

                    for field_name, model in related_models.items():
                        related_data = request.data.get(field_name)
                        if related_data:
                            # Handle single object (OneToOne)
                            if field_name == "current_address":
                                # Remove candidate field if present
                                if "candidate" in related_data:
                                    del related_data["candidate"]
                                if "id" in related_data:
                                    del related_data["id"]
                                
                                # Update or create current address
                                CurrentAddress.objects.update_or_create(
                                    candidate=candidate,
                                    defaults=related_data
                                )
                            # Handle multiple objects (ForeignKey)
                            else:
                                # Delete existing objects
                                model.objects.filter(candidate=candidate).delete()
                                
                                # Create new objects
                                if isinstance(related_data, list):
                                    for item in related_data:
                                        # Remove candidate and id fields if present
                                        if "candidate" in item:
                                            del item["candidate"]
                                        if "id" in item:
                                            del item["id"]
                                        model.objects.create(candidate=candidate, **item)

                return responseWrapper(True, serializer.data, "Candidate and related data updated successfully", 200)

        except Candidate.DoesNotExist:
            return responseWrapper(False, None, "Candidate not found", 404)
        except Exception as e:
            import traceback
            print(traceback.format_exc())  # Print the full error traceback
            return responseWrapper(False, None, f"Error: {str(e)}", 500)

# @swagger_auto_schema(
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'image': openapi.Schema(type=openapi.TYPE_FILE, description='User profile image file')
#         }
#     ),
#     responses={200: "Image uploaded successfully", 400: "Bad request", 404: "Candidate not found"}
# )
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_user_image(request, candidateId):
    try:
        candidate = Candidate.objects.get(id=candidateId)
        
        if 'image' not in request.FILES:
            return responseWrapper(False, None, "No image file provided", 400)
            
        image_file = request.FILES['image']
        
        # Validate file type
        if not image_file.content_type.startswith('image/'):
            return responseWrapper(False, None, "Invalid file type. Only image files are allowed", 400)
            
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'user_images')
        os.makedirs(media_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(image_file.name)[1]
        filename = f"candidate_{candidateId}_image{file_extension}"
        filepath = os.path.join(media_dir, filename)
        
        # Save the file
        with open(filepath, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
                
        # Update candidate's dp_id with the file ID
        candidate.dp_id = filename
        candidate.save()
        
        # Return the full URL including domain
        image_url = request.build_absolute_uri(f"/media/user_images/{filename}")
        return responseWrapper(True, {"image_url": image_url}, "Image uploaded successfully", 200)
        
    except Candidate.DoesNotExist:
        return responseWrapper(False, None, "Candidate not found", 404)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return responseWrapper(False, None, f"Error: {str(e)}", 500)

# @swagger_auto_schema(
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'video': openapi.Schema(type=openapi.TYPE_FILE, description='User profile video file')
#         }
#     ),
#     responses={200: "Video uploaded successfully", 400: "Bad request", 404: "Candidate not found"}
# )
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_profile_video(request, candidateId):
    try:
        candidate = Candidate.objects.get(id=candidateId)
        
        if 'video' not in request.FILES:
            return responseWrapper(False, None, "No video file provided", 400)
            
        video_file = request.FILES['video']
        
        # Validate file type
        if not video_file.content_type.startswith('video/'):
            return responseWrapper(False, None, "Invalid file type. Only video files are allowed", 400)
            
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'profile_videos')
        os.makedirs(media_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(video_file.name)[1]
        filename = f"candidate_{candidateId}_video{file_extension}"
        filepath = os.path.join(media_dir, filename)
        
        # Save the file
        with open(filepath, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
                
        # Update candidate's video_id with the file ID
        candidate.video_id = filename
        candidate.save()
        
        return responseWrapper(True, {"video_url": f"/media/profile_videos/{filename}"}, "Video uploaded successfully", 200)
        
    except Candidate.DoesNotExist:
        return responseWrapper(False, None, "Candidate not found", 404)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return responseWrapper(False, None, f"Error: {str(e)}", 500)

@api_view(['GET'])
def get_candidate_image(request, candidateId):
    try:
        candidate = Candidate.objects.get(id=candidateId)
        
        if not candidate.dp_id:
            return responseWrapper(False, None, "No image found for this candidate", 404)
            
        image_path = os.path.join(settings.MEDIA_ROOT, 'user_images', candidate.dp_id)
        
        if not os.path.exists(image_path):
            return responseWrapper(False, None, "Image file not found", 404)
            
        # Return the full URL including domain
        image_url = request.build_absolute_uri(f"/media/user_images/{candidate.dp_id}")
        return responseWrapper(True, {"image_url": image_url}, "Image retrieved successfully", 200)
        
    except Candidate.DoesNotExist:
        return responseWrapper(False, None, "Candidate not found", 404)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return responseWrapper(False, None, f"Error: {str(e)}", 500)

@api_view(['GET'])
def get_candidate_video(request, candidateId):
    try:
        candidate = Candidate.objects.get(id=candidateId)
        
        if not candidate.video_id:
            return responseWrapper(False, None, "No video found for this candidate", 404)
            
        video_path = os.path.join(settings.MEDIA_ROOT, 'profile_videos', candidate.video_id)
        
        if not os.path.exists(video_path):
            return responseWrapper(False, None, "Video file not found", 404)
            
        return responseWrapper(True, {"video_url": f"/media/profile_videos/{candidate.video_id}"}, "Video retrieved successfully", 200)
        
    except Candidate.DoesNotExist:
        return responseWrapper(False, None, "Candidate not found", 404)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return responseWrapper(False, None, f"Error: {str(e)}", 500)