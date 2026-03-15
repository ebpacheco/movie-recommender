<template>
  <div class="page">
    <div class="bg-overlay"></div>
    <div class="container">
      <div class="header">
        <router-link to="/register" class="back-link">← Voltar</router-link>
        <img src="/logo.svg" alt="CineMagIA" class="logo" />
        <h1>Política de Privacidade</h1>
        <p class="updated">Última atualização: março de 2026</p>
      </div>

      <div class="content">

        <section>
          <h2>1. Controlador dos Dados</h2>
          <p>A <strong>CineMagIA</strong> é responsável pelo tratamento dos dados pessoais coletados em sua plataforma, nos termos da <strong>Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018)</strong>.</p>
          <!-- <p>Para exercer seus direitos ou esclarecer dúvidas sobre o tratamento de dados, entre em contato com o nosso Encarregado de Proteção de Dados (DPO) pelo e-mail: <strong>privacidade@cinemagIA.com</strong></p> -->
        </section>

        <section>
          <h2>2. Dados Coletados</h2>
          <p>Coletamos as seguintes categorias de dados pessoais:</p>

          <h3>2.1 Dados de cadastro</h3>
          <ul>
            <li><strong>Nome completo</strong> — identificação do usuário na plataforma;</li>
            <li><strong>Endereço de e-mail</strong> — comunicação, autenticação e verificação de conta;</li>
            <li><strong>Senha</strong> — armazenada exclusivamente em formato criptografado (bcrypt), nunca em texto simples;</li>
            <li><strong>Data de nascimento</strong> — verificação de elegibilidade de uso;</li>
            <li><strong>País de residência</strong> — personalização das plataformas de streaming disponíveis.</li>
          </ul>

          <h3>2.2 Dados de preferências cinematográficas</h3>
          <ul>
            <li>Gêneros favoritos (até 3);</li>
            <li>Filmes favoritos (até 3);</li>
            <li>Atores favoritos (até 5);</li>
            <li>Diretores favoritos (até 3);</li>
            <li>Plataformas de streaming disponíveis ao usuário.</li>
          </ul>

          <h3>2.3 Dados de uso</h3>
          <ul>
            <li>Prompts de humor/sentimento inseridos pelo usuário ao solicitar recomendações;</li>
            <li>Histórico de recomendações geradas (filmes sugeridos e mensagem da IA);</li>
            <li>Idioma de preferência selecionado;</li>
            <li>Tokens de verificação de e-mail e de redefinição de senha (com validade limitada);</li>
            <li>Data e hora de verificação do e-mail e das atividades na conta.</li>
          </ul>

          <h3>2.4 Dados de segurança</h3>
          <ul>
            <li>Token de score do reCAPTCHA v3 do Google, utilizado para detectar atividades automatizadas durante o login.</li>
          </ul>
        </section>

        <section>
          <h2>3. Base Legal</h2>
          <p>O tratamento dos seus dados pessoais é realizado com base nas seguintes hipóteses previstas na LGPD:</p>
          <ul>
            <li><strong>Consentimento (art. 7º, I):</strong> para tratamento de preferências pessoais e geração de recomendações por IA;</li>
            <li><strong>Execução de contrato (art. 7º, V):</strong> para autenticação, envio de e-mails transacionais e funcionamento da conta;</li>
            <li><strong>Legítimo interesse (art. 7º, IX):</strong> para prevenção a fraudes e segurança da plataforma.</li>
          </ul>
        </section>

        <section>
          <h2>4. Compartilhamento com Terceiros</h2>
          <p>A CineMagIA <strong>não vende</strong> seus dados pessoais. O compartilhamento ocorre apenas com os seguintes parceiros de infraestrutura, estritamente para viabilizar o serviço:</p>

          <h3>4.1 Serviços de Inteligência Artificial</h3>
          <ul>
            <li><strong>Google Gemini API:</strong> recebe o prompt de humor do usuário e preferências cinematográficas (sem dados de identificação pessoal) para gerar recomendações. Sujeito à <a href="https://policies.google.com/privacy" target="_blank">Política de Privacidade do Google</a>.</li>
            <li><strong>OpenAI API:</strong> alternativa ao Gemini, com a mesma limitação de dados transmitidos. Sujeito à <a href="https://openai.com/policies/privacy-policy" target="_blank">Política de Privacidade da OpenAI</a>.</li>
          </ul>

          <h3>4.2 Serviço de E-mail</h3>
          <ul>
            <li><strong>Resend:</strong> utilizado para envio de e-mails transacionais (verificação de conta, redefinição de senha). O endereço de e-mail é compartilhado para entrega da mensagem. Sujeito à <a href="https://resend.com/legal/privacy-policy" target="_blank">Política de Privacidade do Resend</a>.</li>
          </ul>

          <h3>4.3 Proteção contra Bots</h3>
          <ul>
            <li><strong>Google reCAPTCHA v3:</strong> utilizado no login para avaliar o risco de atividade automatizada. O Google processa dados comportamentais do navegador para gerar um score de risco. Sujeito à <a href="https://policies.google.com/privacy" target="_blank">Política de Privacidade do Google</a>.</li>
          </ul>

          <h3>4.4 Infraestrutura</h3>
          <ul>
            <li>A plataforma é hospedada em servidores com banco de dados <strong>PostgreSQL</strong>. Os dados são armazenados de forma segura e acessados apenas pela aplicação.</li>
          </ul>
        </section>

        <section>
          <h2>5. Transferência Internacional de Dados</h2>
          <p>Ao utilizar a CineMagIA, seus dados de preferências e humor podem ser processados por servidores do Google (EUA) e da OpenAI (EUA). Essas transferências ocorrem com salvaguardas adequadas, nos termos do art. 33 da LGPD, pois os destinatários possuem políticas de proteção de dados compatíveis com padrões internacionais.</p>
        </section>

        <section>
          <h2>6. Retenção dos Dados</h2>
          <ul>
            <li><strong>Dados da conta:</strong> mantidos enquanto a conta estiver ativa;</li>
            <li><strong>Preferências cinematográficas:</strong> mantidas enquanto a conta estiver ativa e atualizadas conforme escolha do usuário;</li>
            <li><strong>Histórico de recomendações:</strong> mantido apenas durante a sessão ativa de 3 horas. Após esse período, os dados podem ser excluídos automaticamente da base;</li>
            <li><strong>Tokens de verificação e redefinição:</strong> excluídos automaticamente após uso ou expiração (24h para e-mail, 1h para senha);</li>
            <li><strong>Dados de conta encerrada:</strong> excluídos em até 30 dias após a solicitação de exclusão, salvo obrigação legal de retenção.</li>
          </ul>
        </section>

        <section>
          <h2>7. Segurança dos Dados</h2>
          <p>Adotamos medidas técnicas e organizacionais para proteger seus dados, incluindo:</p>
          <ul>
            <li>Criptografia de senhas com algoritmo <strong>bcrypt</strong>;</li>
            <li>Autenticação via <strong>JWT</strong> com expiração configurada;</li>
            <li>Tokens de segurança com validade limitada e uso único;</li>
            <li>Proteção contra bots via <strong>reCAPTCHA v3</strong>;</li>
            <li>Comunicação via HTTPS;</li>
            <li>Banco de dados não exposto publicamente.</li>
          </ul>
          <p>Apesar das medidas adotadas, nenhum sistema é completamente invulnerável. Em caso de incidente de segurança que afete seus dados, você será notificado conforme exigido pela LGPD.</p>
        </section>

        <section>
          <h2>8. Seus Direitos (LGPD)</h2>
          <p>Nos termos da Lei Geral de Proteção de Dados (art. 18), você tem direito a:</p>
          <ul>
            <li><strong>Confirmação e acesso:</strong> saber quais dados pessoais tratamos sobre você;</li>
            <li><strong>Anonimização, bloqueio ou eliminação:</strong> de dados desnecessários ou tratados em desconformidade com a LGPD;</li>
            <li><strong>Portabilidade:</strong> receber seus dados em formato estruturado;</li>
            <li><strong>Eliminação:</strong> solicitar a exclusão dos dados tratados com base em consentimento;</li>
            <li><strong>Revogação do consentimento:</strong> retirar o consentimento a qualquer momento, sem prejuízo do tratamento realizado anteriormente;</li>
            <li><strong>Oposição:</strong> opor-se ao tratamento realizado com base em legítimo interesse;</li>
            <li><strong>Informação:</strong> sobre as entidades com as quais compartilhamos seus dados.</li>
          </ul>
        </section>

        <section>
          <h2>9. Cookies e Armazenamento Local</h2>
          <p>A CineMagIA utiliza <strong>armazenamento local do navegador (localStorage)</strong> para manter a sessão autenticada do usuário e as preferências de idioma. Não utilizamos cookies de rastreamento, publicidade ou análise comportamental proprietários.</p>
          <p>O Google reCAPTCHA pode definir cookies próprios para avaliação de comportamento. Consulte a política do Google para detalhes.</p>
        </section>

        <section>
          <h2>10. Menores de Idade</h2>
          <p>A plataforma é destinada exclusivamente a usuários com <strong>18 anos ou mais</strong>. Não coletamos intencionalmente dados de menores de 18 anos. Caso identificada uma conta criada por menor de idade, os dados serão excluídos imediatamente e o acesso será revogado.</p>
        </section>

        <section>
          <h2>11. Alterações nesta Política</h2>
          <p>Podemos atualizar esta Política de Privacidade periodicamente. Alterações significativas serão comunicadas por e-mail ou por aviso na plataforma com antecedência mínima de 7 dias. A data de "última atualização" no topo deste documento indica quando a versão vigente foi publicada.</p>
        </section>

        <section>
          <h2>12. Canal de Denúncias</h2>
          <p>Você pode reportar violações à <strong>Autoridade Nacional de Proteção de Dados (ANPD)</strong> pelo site <em>gov.br/anpd</em>.</p>
        </section>

      </div>

      <div class="footer">
        <router-link to="/register" class="btn">Voltar ao cadastro</router-link>
        <router-link to="/terms" class="link">← Ver Termos de Uso</router-link>
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

h3 {
  font-size: 0.88rem;
  color: #b09040;
  margin: 0.25rem 0 0;
  font-weight: 500;
}

p {
  color: #8a7a5a;
  font-size: 0.88rem;
  line-height: 1.75;
  margin: 0;
}

strong { color: #b09040; }

a {
  color: #d4af37;
  text-decoration: none;
}
a:hover { text-decoration: underline; }

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
