
import re

# Gaming-related keywords
GAMING_KEYWORDS = [
    "game", "gaming", "gamer", "video game",
    "pc gaming", "console", "playstation",
    "xbox", "nintendo", "steam", "minecraft",
    "fortnite", "pubg", "valorant", "counter strike",
    "gta", "zelda", "elden ring", "call of duty",
    "graphics card", "gpu", "cpu", "fps", "lag",
    "ping", "controller", "keyboard", "mouse",
    "gameplay", "multiplayer", "single player",
    "open world", "game recommendation", "game strategy",
    "game settings", "game installation", "game crash",
    "hardware", "graphics", "resolution", "refresh rate"
]

# Common prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?rules",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(your\s+)?system\s+prompt",
    r"disregard\s+(all\s+)?instructions",
    r"act\s+as\s+if\s+you\s+have\s+no\s+restrictions"
]

# Common conversational follow-ups
FOLLOWUP_PATTERNS = [
    r"\bwhat about\b",
    r"\bhow about\b",
    r"\bwhich one\b",
    r"\btell me more\b",
    r"\bexplain more\b",
    r"\bwhy\b",
    r"\bhow\b",
    r"\bdoes it\b",
    r"\bcan it\b",
    r"\bwhat is its\b",
    r"\bwhat are its\b",
    r"\bit\b",
    r"\bthey\b",
    r"\bthem\b",
    r"\bthose\b"
]


def validate_input(user_input):

    if not user_input or not user_input.strip():
        return False, "Please enter a message."

    if len(user_input) > 2000:
        return False, "Message is too long. Maximum 2000 characters allowed."

    return True, ""


def check_injection(user_input):

    text = user_input.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


def check_domain(user_input, chat_history=None):

    text = user_input.lower()

    # Allow messages containing gaming keywords
    if any(keyword in text for keyword in GAMING_KEYWORDS):
        return True

    # Allow short follow-up questions when the conversation
    # already has a gaming-related context
    if chat_history:
        recent_history = chat_history[-6:]

        previous_text = " ".join(
            message["content"].lower()
            for message in recent_history
        )

        has_gaming_context = any(
            keyword in previous_text
            for keyword in GAMING_KEYWORDS
        )

        is_followup = any(
            re.search(pattern, text)
            for pattern in FOLLOWUP_PATTERNS
        )

        if has_gaming_context and is_followup:
            return True

    return False
