from dataclasses import dataclass
from typing import Dict, Optional, List
from datetime import datetime
from .enums import EmotionLevel, PetAction, EmotionState, ActionResponse
from .storage import Storage

@dataclass
class PetStatus:
    hunger: float = 50.0      # 饥饿值 (0-100)
    happiness: float = 50.0    # 开心值 (0-100)
    sadness: float = 0.0      # 难过值 (0-100)
    anger: float = 0.0        # 愤怒值 (0-100)
    boredom: float = 0.0      # 无聊值 (0-100)
    health: float = 100.0     # 健康值 (0-100)
    energy: float = 100.0     # 精力值 (0-100)

    def to_dict(self) -> Dict[str, float]:
        return {
            "hunger": self.hunger,
            "happiness": self.happiness,
            "sadness": self.sadness,
            "anger": self.anger,
            "boredom": self.boredom,
            "health": self.health,
            "energy": self.energy
        }

class Pet:
    def __init__(self, name: str):
        self.name = name
        self.status = PetStatus()
        self.current_action = PetAction.RESTING
        self.last_update = datetime.now().timestamp()
        self.storage = Storage()
        
        # 尝试加载保存的数据
        self.load_state()
    
    def save_state(self) -> None:
        """保存当前状态"""
        data = {
            "name": self.name,
            "status": self.status.to_dict(),
            "last_update": self.last_update
        }
        self.storage.save(data)
    
    def load_state(self) -> None:
        """加载保存的状态"""
        data = self.storage.load()
        if data:
            self.name = data["name"]
            self.status = PetStatus(**data["status"])
            self.last_update = data["last_update"]
            self.update_status_by_time()
    
    def update_status_by_time(self) -> None:
        """根据时间更新状态"""
        current_time = datetime.now().timestamp()
        elapsed_hours = (current_time - self.last_update) / 3600  # 转换为小时
        
        if elapsed_hours > 0:
            # 饥饿值随时间增加
            self.status.hunger = min(100, self.status.hunger + elapsed_hours * 5)
            
            # 健康值随时间恢复
            if self.status.health < 100:
                self.status.health = min(100, self.status.health + elapsed_hours * 2)
            
            # 愤怒值随时间降低
            if self.status.anger > 0:
                self.status.anger = max(0, self.status.anger - elapsed_hours * 3)
            
            # 无聊值随时间增加
            self.status.boredom = min(100, self.status.boredom + elapsed_hours * 4)
            
            # 精力值随时间恢复
            if self.status.energy < 100:
                self.status.energy = min(100, self.status.energy + elapsed_hours * 10)
            
            # 更新最后更新时间
            self.last_update = current_time
            
            # 保存更新后的状态
            self.save_state()
        
    def get_emotion_level(self, value: float) -> EmotionLevel:
        if value >= 70:
            return EmotionLevel.HIGH
        elif value >= 30:
            return EmotionLevel.MEDIUM
        return EmotionLevel.LOW

    def get_dominant_emotion(self) -> tuple[EmotionState, EmotionLevel]:
        """返回当前最显著的情绪状态和程度"""
        status_map = {
            EmotionState.HUNGRY: self.status.hunger,
            EmotionState.HAPPY: self.status.happiness,
            EmotionState.SAD: self.status.sadness,
            EmotionState.ANGRY: self.status.anger,
            EmotionState.BORED: self.status.boredom,
            EmotionState.SICK: 100 - self.status.health,
            EmotionState.TIRED: 100 - self.status.energy
        }
        
        dominant_emotion = max(status_map.items(), key=lambda x: x[1])
        return (dominant_emotion[0], self.get_emotion_level(dominant_emotion[1]))

    def can_perform_action(self, action: str) -> bool:
        """检查当前状态是否允许执行某个操作"""
        emotion, level = self.get_dominant_emotion()
        
        # 特定情绪下的行为限制
        restrictions = {
            EmotionState.ANGRY: ['pet', 'shake'],
            EmotionState.SAD: ['feed', 'shake'],
            EmotionState.SICK: ['shake', 'hit'],
            EmotionState.TIRED: ['shake', 'hit', 'pet']
        }
        
        # 如果情绪程度高且有行为限制，检查是否被限制
        if level == EmotionLevel.HIGH and emotion in restrictions:
            return action not in restrictions[emotion]
        return True

    def update_action(self) -> PetAction:
        """根据当前状态更新宠物的行为"""
        emotion, level = self.get_dominant_emotion()
        
        # 根据情绪状态和程度决定行为
        action_map = {
            (EmotionState.HAPPY, EmotionLevel.HIGH): PetAction.DANCING,
            (EmotionState.SAD, EmotionLevel.HIGH): PetAction.CRYING,
            (EmotionState.ANGRY, EmotionLevel.HIGH): PetAction.ANGRY,
            (EmotionState.TIRED, EmotionLevel.HIGH): PetAction.SLEEPING,
            (EmotionState.HUNGRY, EmotionLevel.HIGH): PetAction.EATING,
            (EmotionState.BORED, EmotionLevel.HIGH): PetAction.PLAYING,
            (EmotionState.SICK, EmotionLevel.HIGH): PetAction.SICK
        }
        
        self.current_action = action_map.get((emotion, level), PetAction.RESTING)
        return self.current_action

    def feed(self) -> None:
        """喂食操作"""
        if self.can_perform_action('feed'):
            self.status.hunger = max(0, self.status.hunger - 30)
            self.status.happiness = min(100, self.status.happiness + 10)
            self.status.energy = min(100, self.status.energy + 5)

    def pet(self) -> None:
        """抚摸操作"""
        if self.can_perform_action('pet'):
            self.status.happiness = min(100, self.status.happiness + 15)
            self.status.sadness = max(0, self.status.sadness - 10)
            self.status.anger = max(0, self.status.anger - 10)

    def heal(self) -> None:
        """医疗操作"""
        if self.can_perform_action('heal'):
            self.status.health = min(100, self.status.health + 20)
            self.status.happiness = min(100, self.status.happiness + 5)

    def hit(self) -> None:
        """打击操作"""
        if self.can_perform_action('hit'):
            self.status.anger = min(100, self.status.anger + 30)
            self.status.happiness = max(0, self.status.happiness - 20)
            self.status.health = max(0, self.status.health - 10)

    def shake(self) -> None:
        """摇晃操作"""
        if self.can_perform_action('shake'):
            self.status.boredom = max(0, self.status.boredom - 20)
            self.status.energy = max(0, self.status.energy - 10)
            self.status.happiness = min(100, self.status.happiness + 5)

    def perform_action(self, action: str) -> Optional[ActionResponse]:
        """执行动作并返回动作响应"""
        if not self.can_perform_action(action):
            return ActionResponse.ACTION_REFUSE
            
        action_responses = {
            'feed': ActionResponse.FEED_SUCCESS,
            'pet': ActionResponse.PET_SUCCESS,
            'heal': ActionResponse.HEAL_SUCCESS,
            'shake': ActionResponse.SHAKE_SUCCESS
        }
        
        # 执行动作
        if action == 'feed':
            self.feed()
        elif action == 'pet':
            self.pet()
        elif action == 'heal':
            self.heal()
        elif action == 'hit':
            self.hit()
        elif action == 'shake':
            self.shake()
            
        return action_responses.get(action)