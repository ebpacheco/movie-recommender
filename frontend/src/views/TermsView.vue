<template>
  <div class="page">
    <div class="bg-overlay"></div>
    <div class="container">
      <div class="header">
        <router-link to="/register" class="back-link">← Voltar</router-link>
        <img src="/logo.svg" alt="CineMagIA" class="logo" />
        <h1>Termos de Uso</h1>
        <p class="updated">Última atualização: março de 2026</p>
      </div>

      <div class="content">

        <section>
          <h2>1. Aceitação dos Termos</h2>
          <p>Ao criar uma conta e utilizar a plataforma <strong>CineMagIA</strong>, você declara que leu, compreendeu e concorda com estes Termos de Uso. Se você não concordar com qualquer parte destes termos, não deverá utilizar a plataforma.</p>
          <p>O uso contínuo da plataforma após alterações nos Termos de Uso constitui aceitação das novas condições.</p>
        </section>

        <section>
          <h2>2. Descrição do Serviço</h2>
          <p>A CineMagIA é uma plataforma de recomendação cinematográfica baseada em Inteligência Artificial. O serviço analisa o estado emocional e as preferências pessoais do usuário para sugerir filmes disponíveis em plataformas de streaming.</p>
          <p>As recomendações são geradas por modelos de linguagem de terceiros (Google Gemini ou OpenAI GPT) e são de natureza subjetiva. A CineMagIA não garante que as sugestões atenderão plenamente às expectativas do usuário, pois dependem da qualidade das preferências cadastradas e da interpretação do modelo de IA.</p>
          <p>O serviço está disponível nos idiomas Português, Inglês e Espanhol.</p>
        </section>

        <section>
          <h2>3. Elegibilidade e Cadastro</h2>
          <p>Para utilizar a CineMagIA, o usuário deve:</p>
          <ul>
            <li>Ter no mínimo 18 (dezoito) anos de idade;</li>
            <li>Fornecer informações verdadeiras, precisas e completas no cadastro;</li>
            <li>Manter seus dados atualizados;</li>
            <li>Verificar seu endereço de e-mail por meio do link enviado após o cadastro.</li>
          </ul>
          <p>É proibido criar contas falsas, múltiplas contas para o mesmo usuário ou utilizar dados de terceiros sem autorização. A CineMagIA reserva-se o direito de suspender ou encerrar contas que violem esta regra.</p>
        </section>

        <section>
          <h2>4. Conta e Segurança</h2>
          <p>Você é responsável pela confidencialidade da sua senha e por todas as atividades realizadas em sua conta. Em caso de uso não autorizado, notifique-nos imediatamente.</p>
          <p>A senha deve conter no mínimo 8 caracteres, incluindo letra maiúscula, número e caractere especial. A CineMagIA utiliza o algoritmo <strong>bcrypt</strong> para armazenamento seguro de senhas — elas nunca são armazenadas em texto simples.</p>
          <p>Tokens de verificação de e-mail expiram em 24 horas. Tokens de redefinição de senha expiram em 1 hora. Sessões autenticadas são gerenciadas via <strong>JWT (JSON Web Token)</strong>.</p>
        </section>

        <section>
          <h2>5. Preferências e Personalização</h2>
          <p>Para receber recomendações personalizadas, o usuário deve configurar seu perfil com:</p>
          <ul>
            <li>Gêneros cinematográficos favoritos (mínimo de 3, máximo de 3 selecionados);</li>
            <li>Filmes favoritos (até 3);</li>
            <li>Atores favoritos (até 5);</li>
            <li>Diretores favoritos (até 3);</li>
            <li>Plataformas de streaming disponíveis na sua região (mínimo de 1).</li>
          </ul>
          <p>Essas informações são utilizadas exclusivamente para a geração de recomendações e não são compartilhadas com anunciantes ou terceiros para fins comerciais.</p>
        </section>

        <section>
          <h2>6. Cache de Recomendações</h2>
          <p>Para evitar o consumo excessivo de recursos de IA, as recomendações geradas são armazenadas em cache por <strong>3 horas</strong>. Durante esse período, novas solicitações retornarão os mesmos resultados. Após a expiração do cache, uma nova recomendação poderá ser gerada.</p>
        </section>

        <section>
          <h2>7. Uso Permitido</h2>
          <p>Você pode utilizar a CineMagIA para:</p>
          <ul>
            <li>Descobrir filmes alinhados ao seu estado emocional e preferências;</li>
            <li>Gerenciar e atualizar suas preferências cinematográficas;</li>
            <li>Consultar o histórico de recomendações recebidas;</li>
            <li>Assistir trailers dos filmes recomendados.</li>
          </ul>
        </section>

        <section>
          <h2>8. Uso Proibido</h2>
          <p>É expressamente proibido:</p>
          <ul>
            <li>Utilizar a plataforma para fins ilegais ou que violem direitos de terceiros;</li>
            <li>Tentar burlar sistemas de segurança, autenticação ou proteção anti-bot (reCAPTCHA);</li>
            <li>Realizar engenharia reversa, scraping ou extração automatizada de dados;</li>
            <li>Sobrecarregar intencionalmente os servidores com requisições abusivas;</li>
            <li>Compartilhar credenciais de acesso com terceiros;</li>
            <li>Inserir informações falsas ou enganosas no cadastro.</li>
          </ul>
          <p>O descumprimento dessas regras pode resultar em suspensão ou exclusão permanente da conta, sem prejuízo de medidas legais cabíveis.</p>
        </section>

        <section>
          <h2>9. Propriedade Intelectual</h2>
          <p>Todo o conteúdo da plataforma — incluindo logotipo, design, textos e código — é de propriedade da CineMagIA e está protegido pelas leis de propriedade intelectual brasileiras e internacionais.</p>
          <p>As informações sobre filmes (pôsteres, títulos, sinopses) são obtidas de fontes públicas e de APIs de terceiros. A CineMagIA não reivindica propriedade sobre esses conteúdos.</p>
          <p>O conteúdo gerado pela IA (mensagens de recomendação) é disponibilizado ao usuário para uso pessoal, sem transferência de direitos autorais.</p>
        </section>

        <section>
          <h2>10. Disponibilidade do Serviço</h2>
          <p>A CineMagIA se esforça para manter o serviço disponível 24 horas por dia, 7 dias por semana, mas não garante disponibilidade ininterrupta. Podem ocorrer interrupções por manutenção, atualizações, falhas em serviços de terceiros (IA, e-mail, banco de dados) ou situações de força maior.</p>
          <p>A CineMagIA não se responsabiliza por danos decorrentes de indisponibilidade temporária do serviço.</p>
        </section>

        <section>
          <h2>11. Limitação de Responsabilidade</h2>
          <p>A CineMagIA não se responsabiliza por:</p>
          <ul>
            <li>Decisões tomadas com base nas recomendações geradas pela IA;</li>
            <li>Disponibilidade dos filmes nas plataformas de streaming indicadas;</li>
            <li>Conteúdo dos filmes recomendados;</li>
            <li>Falhas nos serviços de terceiros integrados à plataforma;</li>
            <li>Perda de dados decorrente de caso fortuito ou força maior.</li>
          </ul>
        </section>

        <section>
          <h2>12. Modificações nos Termos</h2>
          <p>A CineMagIA pode modificar estes Termos de Uso a qualquer momento. Alterações relevantes serão comunicadas por e-mail ou por aviso na plataforma com antecedência mínima de 7 dias. O uso continuado da plataforma após esse prazo implica aceitação das novas condições.</p>
        </section>

        <section>
          <h2>13. Encerramento de Conta</h2>
          <p>O usuário pode solicitar o encerramento de sua conta e a exclusão de seus dados a qualquer momento, por meio das configurações da conta ou pelo contato indicado abaixo. Após a exclusão, os dados pessoais serão removidos conforme previsto na Política de Privacidade.</p>
          <p>A CineMagIA pode encerrar contas que violem estes Termos, com ou sem aviso prévio, dependendo da gravidade da infração.</p>
        </section>

        <section>
          <h2>14. Lei Aplicável e Foro</h2>
          <p>Estes Termos de Uso são regidos pelas leis da República Federativa do Brasil. Fica eleito o foro da comarca de São Paulo/SP para dirimir quaisquer controvérsias decorrentes deste instrumento, com renúncia a qualquer outro, por mais privilegiado que seja.</p>
        </section>

        <!-- <section>
          <h2>15. Contato</h2>
          <p>Para dúvidas, sugestões ou solicitações relacionadas a estes Termos de Uso, entre em contato pelo e-mail: <strong>contato@cinemagIA.com</strong></p>
        </section> -->

      </div>

      <div class="footer">
        <router-link to="/register" class="btn">Voltar ao cadastro</router-link>
        <router-link to="/privacy" class="link">Ver Política de Privacidade →</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page {
  min-height: 100vh;
  background: #08080c;
  padding: 3rem 1rem;
  font-family: 'DM Sans', sans-serif;
}

.bg-overlay {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(212, 175, 55, 0.03) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(180, 100, 20, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.back-link {
  position: absolute;
  left: 0;
  top: 0;
  color: #8a7a5a;
  text-decoration: none;
  font-size: 0.85rem;
  transition: color 0.2s;
}
.back-link:hover { color: #d4af37; }

.logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
  filter: drop-shadow(0 0 10px rgba(245, 197, 24, 0.4));
  margin-bottom: 1rem;
}

h1 {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  color: #e8e0d0;
  margin: 0 0 0.5rem;
  font-weight: 600;
}

.updated {
  color: #4a4038;
  font-size: 0.82rem;
  margin: 0;
}

.content {
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.12);
  border-radius: 16px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

section { display: flex; flex-direction: column; gap: 0.75rem; }

h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem;
  color: #d4af37;
  margin: 0;
  font-weight: 600;
}

p {
  color: #8a7a5a;
  font-size: 0.88rem;
  line-height: 1.75;
  margin: 0;
}

strong { color: #b09040; }

ul {
  margin: 0;
  padding-left: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

li {
  color: #8a7a5a;
  font-size: 0.88rem;
  line-height: 1.65;
}

.footer {
  margin-top: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  border-radius: 10px;
  color: #08080c;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}
.btn:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.25); }

.link {
  color: #d4af37;
  font-size: 0.85rem;
  text-decoration: none;
}
.link:hover { text-decoration: underline; }

@media (max-width: 600px) {
  .content { padding: 1.5rem 1.25rem; }
  .back-link { position: static; display: block; margin-bottom: 1rem; }
  h1 { font-size: 1.6rem; }
}
</style>
