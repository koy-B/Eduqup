from django.conf import settings

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None


class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
        if self.api_key and genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def generate_response(self, message: str, context: str = "") -> str:
        if not self.model:
            return "AI service is not configured yet. Add GEMINI_API_KEY to enable responses."

        try:
            prompt = (
                "You are an educational tutor. Keep answers clear, supportive, and focused on mastery.\n\n"
                f"Context:\n{context[:8000]}\n\nStudent Message:\n{message}"
            )
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"AI service error: {str(e)}. Please check your API key and quota."

    def generate_quiz_from_text(self, text: str) -> str:
        if not text.strip():
            return "No extractable text found. Please upload a clearer document."
        if not self.model:
            return (
                "1) Summarize the main concept in your own words.\n"
                "2) List three key terms from the material.\n"
                "3) Create one real-world example related to the topic."
            )

        try:
            prompt = (
                "Create 5 short practice questions to help a student master this material. "
                "Mix conceptual and applied questions.\n\n"
                f"Text:\n{text[:12000]}"
            )
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"AI service error: {str(e)}. Please check your API key and quota."
