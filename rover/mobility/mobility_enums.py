from enum import Enum

class Actions(Enum):
    # Claw:
    claw_lift = 'claw_lift'
    claw_down = 'claw_down'
    
    # Motors:
    m_forward_r = 'm_forward_r'
    m_forward_l = 'm_forward_l'
    m_back_r = 'm_back_r'
    m_back_l = 'm_back_l'
    
    # Predefined actions:
    pivot_l = 'pivot_l'
    pivot_r = 'pivot_r'