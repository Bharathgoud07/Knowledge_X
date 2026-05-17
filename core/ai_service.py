# core/ai_service.py
import logging
import warnings
from django.conf import settings

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)

# Initialize Gemini client if key is available
gemini_model = None
if genai and hasattr(settings, "GEMINI_API_KEY") and settings.GEMINI_API_KEY:
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using gemini-2.5-flash as it is fast and has a free tier
        gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")


def generate_summary(text):
    """
    Generate a summary of the provided text using Gemini.
    Falls back to mock implementation if API key is missing or call fails.
    """
    if not text:
        return ""
    
    if gemini_model:
        try:
            # We truncate the text to ~10000 characters just to be safe with prompt limits,
            # though Gemini 1.5 Flash has a very large context window.
            truncated_text = text[:10000]
            
            prompt = (
                "You are a helpful educational assistant. Summarize the following "
                "educational material into a concise paragraph (max 3 sentences).\n\n"
                f"Text:\n{truncated_text}"
            )
            
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API Error during summary: {str(e)}")
            # Fall through to mock
    
    # Mock fallback
    mock_summary = "This is an AI-generated summary of the document. " \
                   "It covers the key topics extracted from the provided text, " \
                   "giving students a quick overview of the material. " \
                   "(Note: Configure GEMINI_API_KEY for real summaries)"
    return mock_summary


def generate_important_questions(text):
    """
    Generate important questions from the text using Gemini.
    Falls back to mock implementation if API key is missing or call fails.
    """
    if not text:
        return ""
    
    if gemini_model:
        try:
            truncated_text = text[:10000]
            
            prompt = (
                "You are a helpful educational assistant. Generate exactly 3 important "
                "study questions based on the following material. Format them as a numbered list.\n\n"
                f"Text:\n{truncated_text}"
            )
            
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API Error during questions: {str(e)}")
            # Fall through to mock
    
    # Mock fallback
    mock_questions = (
        "1. What are the core concepts discussed in this document?\n"
        "2. How does this topic apply to real-world scenarios?\n"
        "3. Can you explain the main theoretical framework presented?\n"
        "(Note: Configure GEMINI_API_KEY for real questions)"
    )
    return mock_questions


def get_recommendations(resource):
    """
    Get recommended resources based on the subject and keywords.
    Currently using database querying as a basic recommendation engine.
    """
    from resources.models import Resource
    
    if not resource.subject:
        return Resource.objects.none()
        
    return Resource.objects.filter(
        subject=resource.subject,
        verification_status="APPROVED"
    ).exclude(id=resource.id).order_by('-download_count')[:5]


def calculate_ai_ranking_score(resource):
    """
    Calculate an AI ranking score.
    Mock logic: Base score on downloads, ratings, and a random AI 'quality' factor.
    """
    base_score = (resource.download_count * 0.5) + (resource.view_count * 0.1)
    rating_score = resource.average_rating * 10
    
    # Mock AI quality factor (0.8 to 1.2)
    ai_quality_factor = 1.1 
    
    return round((base_score + rating_score) * ai_quality_factor, 2)


def chat_with_document(extracted_pages_dict, chat_history, new_question):
    """
    Send the document text, chat history, and new question to Gemini to get a response.
    Requires Gemini to cite sources as [Page X].
    """
    if not gemini_model:
        return "The AI Assistant is currently unavailable. Please configure the GEMINI_API_KEY."
        
    if not extracted_pages_dict:
        return "I'm sorry, I couldn't read the text of this document. It might be an image or an empty file."

    # Build the document context
    context_parts = []
    for page_num, text in extracted_pages_dict.items():
        if text.strip():
            context_parts.append(f"--- [Page {page_num}] ---\n{text.strip()}")
            
    # We truncate the context to ensure it fits, though Gemini 1.5 Flash can handle huge context
    document_context = "\n\n".join(context_parts)[:300000]

    # Format history
    history_text = ""
    for msg in chat_history[-5:]: # Last 5 turns to save context
        role = "User" if msg['role'] == 'user' else "AI"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are an intelligent AI Assistant helping a student understand a document.
Here is the text of the document, broken down by page numbers:

<document_context>
{document_context}
</document_context>

Here is the recent chat history:
<history>
{history_text}
</history>

User's new question: "{new_question}"

INSTRUCTIONS:
1. Answer the user's question accurately using ONLY the information provided in the <document_context>. 
2. If the answer is not in the document, say "I cannot find the answer to that in this document." Do not hallucinate outside information.
3. CRITICAL: Whenever you use information from the document, you MUST cite the page number inline using exactly this format: [Page X] (where X is the page number). Example: "The mitochondria is the powerhouse of the cell [Page 3]."
4. Be clear, concise, and helpful. Format your response in Markdown.
"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini API Error during chat: {str(e)}")
        return f"An error occurred while generating the response: {str(e)}"

