from enum import Enum, auto

class EmotionLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class PetAction(Enum):
    SLEEPING = ("sleeping", 0)     # 睡觉
    DANCING = ("dancing", 1)       # 跳舞
    CRYING = ("crying", 2)         # 哭泣
    PLAYING = ("playing", 3)       # 玩耍
    EATING = ("eating", 4)         # 进食
    RESTING = ("resting", 5)       # 休息
    ANGRY = ("angry", 6)           # 发脾气
    SICK = ("sick", 7)             # 生病

    def __init__(self, state: str, index: int):
        self._state = state
        self._index = index

    @property
    def state(self):
        return self._state

    @property
    def index(self):
        return self._index

class ActionResponse(Enum):
    FEED_SUCCESS = ("feed_success", 10)    # 开心地吃东西
    PET_SUCCESS = ("pet_success", 11)      # 开心地被摸
    HEAL_SUCCESS = ("heal_success", 12)    # 接受治疗
    SHAKE_SUCCESS = ("shake_success", 13)  # 开心地玩耍
    ACTION_REFUSE = ("refuse", 14)         # 拒绝动作

    def __init__(self, state: str, index: int):
        self._state = state
        self._index = index

    @property
    def state(self):
        return self._state

    @property
    def index(self):
        return self._index

class EmotionState(Enum):
    HAPPY = ("happy", 20)          # 开心
    SAD = ("sad", 21)             # 难过
    ANGRY = ("angry", 22)         # 生气
    HUNGRY = ("hungry", 23)       # 饥饿
    TIRED = ("tired", 24)         # 疲倦
    BORED = ("bored", 25)         # 无聊
    SICK = ("sick", 26)           # 生病

    def __init__(self, state: str, index: int):
        self._state = state
        self._index = index

    @property
    def state(self):
        return self._state

    @property
    def index(self):
        return self._index