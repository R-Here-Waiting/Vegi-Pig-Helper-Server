from flask import Blueprint, jsonify, request
from app.models.pet import Pet
from app.models.enums import ActionResponse

pet_bp = Blueprint('pet', __name__)
pet = Pet("默认宠物")

@pet_bp.route('/status', methods=['GET'])
def get_status():
    pet.update_status_by_time()
    emotion, level = pet.get_dominant_emotion()
    current_action = pet.update_action()
    
    return jsonify({
        "status": pet.status.to_dict(),
        "emotion": {
            "state": emotion.state,
            "level": level.value,
            "index": emotion.index
        },
        "action": {
            "state": current_action.state,
            "index": current_action.index
        },
        "last_update": pet.last_update
    })

@pet_bp.route('/action', methods=['POST'])
def perform_action():
    pet.update_status_by_time()
    
    action = request.json.get('action')
    
    if action in ['feed', 'pet', 'heal', 'hit', 'shake']:
        action_response = pet.perform_action(action)
        emotion, level = pet.get_dominant_emotion()
        current_action = pet.update_action()
        
        pet.save_state()
        
        response = {
            "status": pet.status.to_dict(),
            "emotion": {
                "state": emotion.state,
                "level": level.value,
                "index": emotion.index
            },
            "action": {
                "state": current_action.state,
                "index": current_action.index
            },
            "last_update": pet.last_update
        }
        
        if action_response:
            response.update({
                "success": action_response != ActionResponse.ACTION_REFUSE,
                "response": {
                    "state": action_response.state,
                    "index": action_response.index
                },
                "message": (f"Successfully performed {action}" 
                          if action_response != ActionResponse.ACTION_REFUSE 
                          else f"Pet refuses to perform {action}")
            })
            
        return jsonify(response)
    
    return jsonify({"error": "Invalid action"}), 400