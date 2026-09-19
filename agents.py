import os
import base64
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# API CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = None

if api_key:
    client = OpenAI(api_key=api_key)


# ============================================================
# TEXT AI
# ============================================================

def ai_request(prompt):

    if not client:
        return None

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        print("AI Error:", e)

        return None


# ============================================================
# VISION AI — FOOD IMAGE ANALYSIS
# ============================================================

def analyze_food_image(image_bytes):

    if not client:
        return {
            "food_name": "Unknown Food",
            "category": "Cooked Food",
            "description": "Image uploaded successfully.",
            "confidence": "Medium"
        }

    try:

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        response = client.responses.create(

            model="gpt-5.6-luna",

            input=[
                {
                    "role": "user",

                    "content": [

                        {
                            "type": "input_text",

                            "text": """
                            Analyze this food image for a food
                            donation management system.

                            Identify:

                            1. Food name
                            2. Food category
                            3. Short description
                            4. Confidence level

                            Do not make claims about food safety
                            from appearance alone.

                            Return the answer in this format:

                            Food Name:
                            Category:
                            Description:
                            Confidence:
                            """
                        },

                        {
                            "type": "input_image",

                            "image_url": (
                                f"data:image/jpeg;base64,"
                                f"{encoded_image}"
                            )
                        }

                    ]
                }
            ]
        )

        text = response.output_text

        return {
            "food_name": text,
            "category": "AI Detected Food",
            "description": text,
            "confidence": "AI Generated"
        }

    except Exception as e:

        print("Vision Error:", e)

        return {
            "food_name": "Food Image",
            "category": "Cooked Food",
            "description": "Unable to analyze image.",
            "confidence": "Unknown"
        }


# ============================================================
# AGENT 1 — FOOD ANALYSIS
# ============================================================

def food_analysis_agent(
    food_name,
    quantity,
    hours_old
):

    prompt = f"""
    You are the Food Analysis Agent.

    Analyze this surplus food:

    Food: {food_name}
    Quantity: {quantity}
    Hours since cooked: {hours_old}

    Provide:

    Food Category:
    Donation Priority:
    Recommended Action:

    Important:
    Do not claim that food is safe or unsafe solely
    based on age or appearance. Recommend appropriate
    food-safety verification.

    Keep the answer concise.
    """

    result = ai_request(prompt)

    if result:

        return result

    # Fallback

    if hours_old <= 4:

        priority = "HIGH"

    elif hours_old <= 8:

        priority = "MEDIUM"

    else:

        priority = "LOW"

    return f"""
Food Category: Cooked Food

Donation Priority: {priority}

Recommended Action:
Arrange donation promptly and verify appropriate
food-safety conditions before distribution.
"""


# ============================================================
# AGENT 2 — RECIPIENT MATCHING
# ============================================================

# ============================================================
# AGENT 2 — RECIPIENT MATCHING
# ============================================================

def matching_agent(
    food_name,
    quantity,
    location
):

    prompt = f"""
You are the Recipient Matching Agent of FoodShare AI.

Your job is to select the MOST APPROPRIATE recipient
for a surplus food donation.

Donation details:

Food: {food_name}
Quantity: {quantity} packets/units
Location: {location}

Possible recipient types:

1. NGO
2. Food Bank
3. Community Kitchen
4. Shelter
5. Orphanage
6. Community Center
7. Nearby Families

Use the following reasoning:

- Large quantities → Food Bank, NGO or Community Kitchen
- Cooked meals → Community Kitchen, Shelter or nearby families
- Packaged food → Food Bank or NGO
- Bread / bakery items → NGO, Food Bank or Community Center
- Small quantities → Nearby Families or Community Center
- Food suitable for children → Orphanage or NGO
- Consider the provided location when recommending the recipient.

IMPORTANT:
Do NOT always recommend a shelter.

Choose the recipient based on the actual donation.

Return the answer in this format:

Recommended Recipient:
Reason:
Suggested Action:

Keep the answer concise.
"""

    result = ai_request(prompt)

    if result:
        return result


    # ========================================================
    # SMART FALLBACK
    # ========================================================

    food = food_name.lower()


    # Packaged food

    if any(word in food for word in [
        "biscuit",
        "cookie",
        "packet",
        "chips",
        "cereal",
        "snack"
    ]):

        if quantity >= 30:

            return (
                "Recommended Recipient: Food Bank\n\n"
                "Reason: The donation is packaged food "
                "and the quantity is suitable for centralized "
                "food distribution.\n\n"
                "Suggested Action: Contact a nearby food bank "
                "or NGO for collection."
            )

        else:

            return (
                "Recommended Recipient: Nearby NGO\n\n"
                "Reason: The packaged food can be distributed "
                "through a local community organization.\n\n"
                "Suggested Action: Arrange local collection."
            )


    # Bread / bakery

    elif any(word in food for word in [
        "bread",
        "bun",
        "cake",
        "bakery",
        "pastry"
    ]):

        return (
            "Recommended Recipient: Community Center / NGO\n\n"
            "Reason: Bakery items can be distributed quickly "
            "through local community organizations.\n\n"
            "Suggested Action: Arrange prompt collection."
        )


    # Cooked rice / biryani / meals

    elif any(word in food for word in [
        "rice",
        "biryani",
        "meal",
        "curry",
        "dal",
        "food",
        "pulao"
    ]):

        if quantity >= 50:

            return (
                "Recommended Recipient: Community Kitchen\n\n"
                "Reason: The large quantity of cooked food "
                "is suitable for organized meal distribution.\n\n"
                "Suggested Action: Contact a community kitchen "
                "for prompt collection."
            )

        else:

            return (
                "Recommended Recipient: Nearby NGO / Community Group\n\n"
                "Reason: The quantity is suitable for local "
                "community distribution.\n\n"
                "Suggested Action: Arrange prompt collection."
            )


    # Milk / drinks

    elif any(word in food for word in [
        "milk",
        "juice",
        "drink",
        "beverage"
    ]):

        return (
            "Recommended Recipient: NGO / Community Center\n\n"
            "Reason: These items can be distributed through "
            "local community support organizations.\n\n"
            "Suggested Action: Arrange collection."
        )


    # Default

    else:

        if quantity >= 50:

            return (
                "Recommended Recipient: NGO / Food Bank\n\n"
                "Reason: The large quantity makes centralized "
                "distribution appropriate.\n\n"
                "Suggested Action: Contact a local NGO or food bank."
            )

        elif quantity >= 20:

            return (
                "Recommended Recipient: Community Center\n\n"
                "Reason: The quantity is suitable for "
                "community-level distribution.\n\n"
                "Suggested Action: Arrange local collection."
            )

        else:

            return (
                "Recommended Recipient: Nearby Community Group\n\n"
                "Reason: The smaller donation is suitable "
                "for local distribution.\n\n"
                "Suggested Action: Arrange a nearby pickup."
            )


# ============================================================
# AGENT 3 — ACTION AGENT
# ============================================================

def action_agent(
    priority,
    recipient
):

    prompt = f"""
    You are the Donation Action Agent.

    Priority:
    {priority}

    Recommended Recipient:
    {recipient}

    Create a short action plan.

    Include:

    Action:
    Status:

    Keep it concise.
    """

    result = ai_request(prompt)

    if result:

        return result

    if priority == "HIGH":

        return """
Action:
Contact the recommended recipient and arrange
pickup promptly.

Status:
Urgent Donation
"""

    elif priority == "MEDIUM":

        return """
Action:
Contact the recipient and schedule pickup.

Status:
Donation Pending
"""

    else:

        return """
Action:
Identify a suitable recipient and arrange donation
after appropriate food-safety verification.

Status:
Donation Pending
"""


# ============================================================
# MULTI-AGENT ORCHESTRATOR
# ============================================================

def run_foodshare_agents(
    food_name,
    quantity,
    location,
    hours_old
):

    # Agent 1

    analysis = food_analysis_agent(
        food_name,
        quantity,
        hours_old
    )

    # Priority

    if hours_old <= 4:

        priority = "HIGH"

    elif hours_old <= 8:

        priority = "MEDIUM"

    else:

        priority = "LOW"

    # Agent 2

    recipient = matching_agent(
        food_name,
        quantity,
        location
    )

    # Agent 3

    action = action_agent(
        priority,
        recipient
    )

    return {

        "analysis": analysis,

        "priority": priority,

        "recipient": recipient,

        "action": action

    }