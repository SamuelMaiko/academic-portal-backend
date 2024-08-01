import random

from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.models import RegistrationCode


class TestRegCodesView(APIView):

    def get(self,request):
        random_code=generate_random_word_code()

        try:
            registration_code = RegistrationCode.objects.create(code=random_code)
            context = {
                'code': registration_code.code
            }
            return render(request, 'a_userauth/test_registration_code.html', context)
        except IntegrityError:
            # Handle the error, e.g., show an error message or log it
            return Response({'message': 'Registration code already exists.'}, status=400)
        
WORDS = [
"alpha", "beta", "gamma", "delta", "epsilon",
"zeta", "eta", "theta", "iota", "kappa",
"lambda", "mu", "nu", "xi", "omicron",
"pi", "rho", "sigma", "tau", "upsilon",
"phi", "chi", "psi", "omega",
"nova", "pulse", "flare", "quasar", "stardust",
"nebula", "comet", "galaxy", "asteroid", "eclipse",
"orbit", "lunar", "solar", "meteor", "horizon",
"cosmos", "zenith", "aurora", "vortex", "pulsar",
"luminous", "radiant", "spark", "glow", "shimmer",
"glint", "twilight", "dawn", "dusk", "eclipse",
"horizon", "zenith", "aurora", "celestial", "stellar"
]

def generate_random_word_code(word_count=2):
    """Generate a random code using a specified number of words."""
    return '-'.join(random.choice(WORDS) for _ in range(word_count))