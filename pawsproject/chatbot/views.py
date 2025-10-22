# chatbot/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def pet_assistant(request):
    if request.method == 'POST':
        # Si es un mensaje del chat
        if 'message' in request.POST:
            user_message = request.POST.get('message', '').strip()
            pet_profile = request.session.get('pet_profile', {})
            
            if not user_message:
                return JsonResponse({'error': 'Mensaje vacío'}, status=400)

            # Construir contexto del perfil
            if pet_profile:
                context = (
                    f"La mascota se llama {pet_profile['name']}, es un/a {pet_profile['type']}, "
                    f"raza: {pet_profile['breed']}, edad: {pet_profile['age']} años, "
                    f"peso: {pet_profile['weight']} kg. "
                )
            else:
                context = ""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Eres un asistente experto en cuidado de mascotas. "
                                "Usa el contexto de la mascota si está disponible. "
                                "Responde en español, de forma clara, útil y empática. "
                                "Si no sabes algo, sugiere consultar a un veterinario."
                            )
                        },
                        {"role": "user", "content": context + user_message}
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )
                bot_reply = response.choices[0].message.content.strip()
                return JsonResponse({'reply': bot_reply})

            except Exception as e:
                logger.error(f"OpenAI error: {str(e)}")
                return JsonResponse({'error': 'No pude procesar tu pregunta. Inténtalo de nuevo.'}, status=500)

        # Si es el envío del formulario
        else:
            pet_data = {
                'name': request.POST.get('pet_name', 'tu mascota'),
                'type': request.POST.get('pet_type', 'mascota'),
                'age': request.POST.get('pet_age', '?'),
                'breed': request.POST.get('pet_breed', 'desconocida'),
                'weight': request.POST.get('pet_weight', '?'),
            }
            # ✅ GUARDAR EN SESIÓN
            request.session['pet_profile'] = pet_data
            return render(request, 'chatbot/chat_interface.html', {'pet_profile': pet_data})

    # GET → mostrar formulario
    return render(request, 'chatbot/pet_form.html')

# En views.py, añade:
def pet_assistant_reset(request):
    if 'pet_profile' in request.session:
        del request.session['pet_profile']
    return redirect('pet_assistant')