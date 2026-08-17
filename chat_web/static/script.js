const chatEl = document.getElementById("chat");
const formEl = document.getElementById("composer");
const inputEl = document.getElementById("input-mensagem");
const btnEnviar = document.getElementById("btn-enviar");
const btnNovoChat = document.getElementById("btn-novo-chat");

function scrollParaFinal() {
  chatEl.scrollTop = chatEl.scrollHeight;
}

function criarMensagem(tipo) {
  // tipo: "user" | "agent" | "erro"
  const msg = document.createElement("div");
  msg.className = `msg msg--${tipo === "erro" ? "erro" : tipo}`;
  return msg;
}

function adicionarMensagemUsuario(texto) {
  const msg = criarMensagem("user");
  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.textContent = texto;
  msg.appendChild(bubble);
  chatEl.appendChild(msg);
  scrollParaFinal();
}

function adicionarMensagemCarregando() {
  const msg = criarMensagem("agent");
  msg.classList.add("msg--loading");
  msg.id = "msg-carregando";
  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.innerHTML = 'Consultando os manuais<span class="dots"><span>.</span><span>.</span><span>.</span></span>';
  msg.appendChild(bubble);
  chatEl.appendChild(msg);
  scrollParaFinal();
}

function removerMensagemCarregando() {
  const el = document.getElementById("msg-carregando");
  if (el) el.remove();
}

function adicionarMensagemAgente(resposta, fontes) {
  const msg = criarMensagem("agent");
  const wrap = document.createElement("div");
  wrap.className = "msg-wrap";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.textContent = resposta;
  wrap.appendChild(bubble);

  if (fontes && fontes.length > 0) {
    const fontesEl = document.createElement("div");
    fontesEl.className = "fontes";

    fontes.forEach((fonte, i) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "fonte-chip";

      const pagina = fonte.pagina ? ` · p.${fonte.pagina}` : "";
      chip.innerHTML =
        `<span class="fonte-arquivo">${escapeHtml(fonte.arquivo)}</span>` +
        `<span class="fonte-pagina">${escapeHtml(pagina)}</span>`;

      const trechoEl = document.createElement("div");
      trechoEl.className = "fonte-trecho";
      trechoEl.textContent = fonte.trecho;
      trechoEl.id = `trecho-${Date.now()}-${i}`;

      chip.addEventListener("click", () => {
        trechoEl.classList.toggle("aberto");
      });

      const col = document.createElement("div");
      col.appendChild(chip);
      col.appendChild(trechoEl);
      fontesEl.appendChild(col);
    });

    wrap.appendChild(fontesEl);
  }

  msg.appendChild(wrap);
  chatEl.appendChild(msg);
  scrollParaFinal();
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function enviarMensagem(texto) {
  adicionarMensagemUsuario(texto);
  adicionarMensagemCarregando();
  btnEnviar.disabled = true;

  try {
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: texto }),
    });
    const dados = await resp.json();

    removerMensagemCarregando();

    if (!resp.ok) {
      const msg = criarMensagem("erro");
      const bubble = document.createElement("div");
      bubble.className = "msg-bubble";
      bubble.textContent = dados.erro || "Ocorreu um erro ao consultar o agente.";
      msg.appendChild(bubble);
      chatEl.appendChild(msg);
      scrollParaFinal();
      return;
    }

    adicionarMensagemAgente(dados.resposta, dados.fontes);
  } catch (err) {
    removerMensagemCarregando();
    const msg = criarMensagem("erro");
    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";
    bubble.textContent = "Não foi possível conectar ao servidor. Verifique se o app.py está em execução.";
    msg.appendChild(bubble);
    chatEl.appendChild(msg);
    scrollParaFinal();
  } finally {
    btnEnviar.disabled = false;
  }
}

formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  const texto = inputEl.value.trim();
  if (!texto) return;
  inputEl.value = "";
  inputEl.style.height = "auto";
  enviarMensagem(texto);
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    formEl.requestSubmit();
  }
});

inputEl.addEventListener("input", () => {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 140) + "px";
});

btnNovoChat.addEventListener("click", async () => {
  await fetch("/api/novo-chat", { method: "POST" });
  chatEl.innerHTML = "";
  const msg = criarMensagem("agent");
  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.textContent = "Novo chat iniciado. Pode perguntar!";
  msg.appendChild(bubble);
  chatEl.appendChild(msg);
});
