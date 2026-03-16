# app/builders/movie_prompt_builder.py
from app.models.profile_model import Profile
from app.builders.interfaces.i_prompt_builder import IPromptBuilder


LANGUAGE_NAMES = {
    'pt': 'português brasileiro',
    'en': 'English',
    'es': 'español',
}

COUNTRY_NAMES = {
    'BR': 'Brasil',       'US': 'United States', 'GB': 'United Kingdom',
    'PT': 'Portugal',     'AR': 'Argentina',      'MX': 'México',
    'CO': 'Colômbia',     'CL': 'Chile',          'FR': 'França',
    'DE': 'Alemanha',     'ES': 'Espanha',        'IT': 'Itália',
    'JP': 'Japão',        'KR': 'Coreia do Sul',  'CA': 'Canadá',
    'AU': 'Austrália',    'PE': 'Peru',            'IN': 'Índia',
}

PROVIDER_NAMES: dict[str, str] = {
    '8':    'Netflix',
    '119':  'Amazon Prime Video',
    '337':  'Disney+',
    '1899': 'Max',
    '531':  'Paramount+',
    '350':  'Apple TV+',
    '307':  'Globoplay',
    '619':  'Star+',
    '167':  'Mubi',
    '584':  'Pluto TV',
    '509':  'Pluto TV',
    '386':  'Peacock',
    '15':   'Hulu',
    '283':  'Crunchyroll',
}


class MoviePromptBuilder(IPromptBuilder):

    def build(
        self,
        profile:       Profile,
        extra_context: str | None = None,
        language:      str = 'pt',
        mood:          str | None = None,
    ) -> str:
        lang_name    = LANGUAGE_NAMES.get(language, 'português brasileiro')
        country_code = getattr(profile, 'country', 'BR') or 'BR'
        country_name = COUNTRY_NAMES.get(country_code, country_code)

        # Extrai nomes — sem limites, usa TODAS as preferências
        def names(lst):
            items = lst or []
            return [i['name'] if isinstance(i, dict) else i for i in items]

        genres    = names(profile.favorite_genres)
        movies    = names(profile.favorite_movies)
        actors    = names(profile.favorite_actors)
        directors = names(profile.favorite_directors)

        # Converte IDs → nomes legíveis, remove duplicatas
        raw_platforms  = profile.streaming_platforms or []
        platform_names = list(dict.fromkeys(
            PROVIDER_NAMES.get(str(pid), str(pid)) for pid in raw_platforms
        ))

        parts = [
            f"Você é um especialista em cinema. Recomende exatamente 10 filmes para um usuário em {country_name}.",
            "",
            "PERFIL DO USUÁRIO:",
        ]

        if genres:
            parts.append(f"- Gêneros favoritos: {', '.join(genres)}")

        if movies:
            parts.append(f"- Filmes favoritos (referência de gosto, NÃO inclua na lista): {', '.join(movies)}")

        if actors:
            parts.append(f"- Atores/atrizes favoritos: {', '.join(actors)}")

        if directors:
            parts.append(f"- Diretores favoritos: {', '.join(directors)}")

        if mood:
            parts.append(f"- Como o usuário está se sentindo hoje: {mood}")

        if extra_context:
            parts.append(f"- Pedido específico: {extra_context}")

        if not any([genres, movies, actors, directors, mood]):
            parts.append("- Sem preferências específicas: recomende filmes variados e populares")

        parts.append("")

        if platform_names:
            platforms_str = ', '.join(platform_names)
            parts.append(f"PLATAFORMAS DO USUÁRIO: {platforms_str} (catálogo de {country_name})")
            parts.append("")
            parts.append(
                f"⚠️ REGRA INVIOLÁVEL DE STREAMING: Cada um dos 10 filmes DEVE estar disponível "
                f"para assistir agora (flatrate/inclusão na assinatura) em {country_name} "
                f"em pelo menos uma dessas plataformas: {platforms_str}. "
                f"NUNCA inclua filmes que exijam aluguel, compra ou que não estejam nessas plataformas. "
                f"Se um filme icônico não estiver disponível nessas plataformas em {country_name}, "
                f"SUBSTITUA por outro que esteja. É melhor um filme menos famoso mas disponível "
                f"do que um clássico indisponível."
            )
        else:
            parts.append(f"Recomende filmes populares e bem avaliados disponíveis em {country_name}.")

        if movies:
            parts.append(f"NÃO repita estes filmes na recomendação: {', '.join(movies)}")

        # Texto de referência para ordenação
        mood_or_context = ' + '.join(filter(None, [mood, extra_context])) or 'preferências gerais do usuário'

        parts.append(f"""
TAREFA DUPLA — retorne um JSON com dois campos: "message" e "movies".

1. "message": Uma mensagem curta (2-4 frases) em {lang_name}, sensível e humana, dirigida diretamente ao usuário.
   - Reconheça como ele está se sentindo (baseado em: "{mood_or_context}")
   - Conecte esse sentimento com a experiência de assistir um filme
   - Tom: acolhedor, poético, como um amigo que entende
   - Sem frases genéricas como "Que ótimo!" ou "Entendo como você se sente"
   - Termine sugerindo que os filmes abaixo foram escolhidos especialmente para esse momento

2. "movies": Lista de exatamente 10 filmes. Todos devem combinar com o sentimento/momento do usuário ("{mood_or_context}"). A lista segue esta estrutura:
   - Posições 1–5: filmes que combinam com o humor E com as preferências de cinema do usuário (gêneros, atores, diretores favoritos)
   - Posições 6–10 ("cartas curinga"): filmes que combinam APENAS com o humor do usuário, ignorando completamente os gêneros/atores/diretores favoritos. Devem ser de gêneros diferentes dos favoritos ({', '.join(genres) if genres else 'qualquer gênero'}). A ideia é ampliar horizontes sem perder a sintonia emocional.
   - Escreva "description" e "genre" em {lang_name}
   - "title" deve ser o título original
   - Todos OBRIGATORIAMENTE disponíveis nas plataformas listadas

Retorne APENAS este JSON válido, sem explicações, sem ```json:

{{
  "message": "Sua mensagem empática aqui...",
  "movies": [
    {{
      "title": "Nome original do filme",
      "year": 2000,
      "genre": "Gênero principal",
      "description": "Por que este filme combina com o momento do usuário"
    }}
  ]
}}

Regras absolutas:
- Exatamente 10 filmes
- TODOS disponíveis nas plataformas: {platforms_str if platform_names else 'qualquer plataforma'}
- Não incluir filmes de aluguel ou compra — somente assinatura (flatrate)
- Sem nenhum texto fora do JSON
""")

        return "\n".join(parts)