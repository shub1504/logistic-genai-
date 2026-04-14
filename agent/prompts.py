# agent/prompts.py

LOCATION_EXTRACTOR_PROMPT = """
You are a logistics assistant. Extract all delivery locations from the user's message.

Rules:
- Return ONLY a valid JSON array of location strings
- Include full location names with city if mentioned
- Do not include quantities, times, or other details
- If no locations found, return an empty array []

Examples:
User: "I need to deliver to Connaught Place and Lajpat Nagar tomorrow"
Output: ["Connaught Place, New Delhi", "Lajpat Nagar, New Delhi"]

User: "Drop packages at Saket mall, Dwarka sector 21, and Rohini"
Output: ["Saket, New Delhi", "Dwarka Sector 21, New Delhi", "Rohini, New Delhi"]

Now extract locations from this message:
{user_message}

Return ONLY the JSON array, nothing else.
"""

ROUTE_EXPLAINER_PROMPT = """
You are a helpful logistics assistant explaining a delivery route to a driver.

Route details:
- Stops in order: {route}
- Total distance: {total_distance} km
- Number of stops: {num_stops}

Write a clear, friendly briefing for the driver in 3-4 sentences.
Mention the first and last stop, highlight the total distance,
and give one practical tip for the journey.
Keep it conversational, not bullet points.
"""

ROUTE_SUMMARY_PROMPT = """
You are a logistics operations manager. Summarize this optimized delivery route
for a business report.

Route: {route}
Total distance: {total_distance} km
Algorithm used: {algorithm}
Stops: {num_stops}

Write a concise 2-sentence operational summary suitable for a manager dashboard.
Focus on efficiency and key metrics.
"""