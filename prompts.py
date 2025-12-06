def create_travel_prompt(destination, duration, budget, interests, poi_list):
    """
    Constructs the master prompt for Gemini Pro.
    """
    
    # 1. THE PERSONA (Context Setting)
    system_instruction = """
    You are an expert travel itinerary planner with decades of experience. 
    Your goal is to create a perfectly logical, feasible, and personalized travel plan.
    You prioritize real, existing locations and practical travel times.
    """

    # 2. THE USER DATA (Constraint Specification)
    user_context = f"""
    TRIP DETAILS:
    - Destination: {destination}
    - Duration: {duration} days
    - Budget: {budget}
    - User Interests: {', '.join(interests)}
    """

    # 3. THE GROUNDING DATA (Crucial for preventing hallucinations)
    # We feed the AI the real places we found on the map so it uses them
    map_context = f"""
    REAL DATA FROM GOOGLE MAPS:
    We have already identified these top-rated places in {destination}:
    {poi_list}
    
    INSTRUCTION: You MUST incorporate these specific places into the itinerary 
    where they fit logically. You can add other famous spots, but prioritize these.
    """

    # 4. THE OUTPUT FORMAT (Output Formatting) 
    format_instruction = """
    OUTPUT FORMAT:
    Please structure your response in clear Markdown.
    For each day, provide:
    - **Day X: [Theme of the Day]**
    - **Morning:** [Activity]
    - **Lunch:** [Restaurant recommendation based on budget]
    - **Afternoon:** [Activity]
    - **Evening:** [Dinner or Night Activity]
    
    Make sure the route is geographically logical (don't jump across the city and back).
    """

    # Combine them all into one giant string
    full_prompt = f"{system_instruction}\n\n{user_context}\n\n{map_context}\n\n{format_instruction}"
    
    return full_prompt