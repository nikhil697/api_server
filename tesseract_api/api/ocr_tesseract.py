import pytesseract
from PIL import Image

def image_to_text(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error in image_to_text: {e}")
        return None

def image_to_bboxes(image, bbox_type):
    try:
        psm_mode = {"word": 8, "line": 7, "paragraph": 4, "block": 6, "page": 1}.get(bbox_type, 6)
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
                "page_num": int(bbox_data[5])
            })
        
        return bbox_list
    except Exception as e:
        print(f"Error in image_to_bboxes: {e}")
        return None
