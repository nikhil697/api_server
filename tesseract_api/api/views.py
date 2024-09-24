import json
import base64
import pytesseract
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def decode_base64_image(base64_str):
    try:
        image_data = base64.b64decode(base64_str)
        Image.open(BytesIO(image_data))  
        return Image.open(BytesIO(image_data))
    except Exception as e:
        logger.error(f"Error decoding base64 image: {str(e)}")
        raise ValueError("Invalid base64_image.")

@csrf_exempt
def get_text(request):
    if request.method == 'POST':
        try:
            logger.info(f"Received data: {request.body}")
            data = json.loads(request.body)
            base64_image = data.get('base64_image')
            
            if not base64_image:
                raise ValueError("No base64_image provided")
            
            image = decode_base64_image(base64_image)
            text = pytesseract.image_to_string(image)
            
            return JsonResponse({'success': True, 'result': {'text': text}})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'success': False, 'error': {'message': "Invalid JSON in request body"}}, status=400)
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            return JsonResponse({'success': False, 'error': {'message': str(e)}}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in get_text: {str(e)}")
            return JsonResponse({'success': False, 'error': {'message': "An unexpected error occurred"}}, status=500)
    else:
        return JsonResponse({'success': False, 'error': {'message': "Only POST method is allowed"}}, status=405)
@csrf_exempt
def get_bboxes(request):
    if request.method == 'POST':
        try:
            logger.info(f"Received data: {request.body}")
            data = json.loads(request.body)
            base64_image = data.get('base64_image')
            bbox_type = data.get('bbox_type')

            if not bbox_type:
                raise ValueError("No bbox_type provided")

            image = decode_base64_image(base64_image)
            psm_mode = {"word": 8, "line": 7, "paragraph": 4, "block": 6, "page": 1}.get(bbox_type)
            
            if psm_mode is None:
                raise ValueError(f"Invalid bbox_type: {bbox_type}")

            config = f'--psm {psm_mode}'
            bboxes = pytesseract.image_to_boxes(image, config=config)

            bbox_list = []
            for bbox in bboxes.splitlines():
                bbox_data = bbox.split()
                bbox_list.append({
                    "character": bbox_data[0],
                    "x_min": int(bbox_data[1]),
                    "y_min": int(bbox_data[2]),
                    "x_max": int(bbox_data[3]),
                    "y_max": int(bbox_data[4]),
                    "page_num": int(bbox_data[5]) if len(bbox_data) > 5 else 0
                })

            return JsonResponse({'success': True, 'result': {'bboxes': bbox_list}})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'success': False, 'error': {'message': "Invalid JSON in request body"}}, status=400)
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            return JsonResponse({'success': False, 'error': {'message': str(e)}}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in get_bboxes: {str(e)}")
            return JsonResponse({'success': False, 'error': {'message': "An unexpected error occurred"}}, status=500)
    else:
        return JsonResponse({'success': False, 'error': {'message': "Only POST method is allowed"}}, status=405)
