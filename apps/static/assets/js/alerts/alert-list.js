(() => {
  let ultimoCreatedAt = null;
  let dataTable = null;

  const tipoEstilo = {
    Informacao:   { cor: "text-primary",     icone: "bi-info-circle",        texto: "Informação" },
    Erro:         { cor: "text-danger",      icone: "bi-exclamation-triangle",texto: "Erro" },
    Sucesso:      { cor: "text-success",     icone: "bi-check-circle",       texto: "Sucesso" },
    Alerta:       { cor: "text-warning",     icone: "bi-exclamation-circle", texto: "Alerta" },
    Debug:        { cor: "text-muted",       icone: "bi-terminal",           texto: "Debug" },
    Timeout:      { cor: "text-dark",        icone: "bi-hourglass-split",    texto: "Timeout" },
    Validacao:    { cor: "text-info",        icone: "bi-shield-check",       texto: "Validação" },
    Interrupcao:  { cor: "text-dark",        icone: "bi-slash-circle",       texto: "Interrupção" },
  };

  const formatarData = (isoString) => {
    const dt = new Date(isoString);
    const dia = String(dt.getDate()).padStart(2, "0");
    const mes = String(dt.getMonth() + 1).padStart(2, "0");
    const ano = dt.getFullYear();
    const hora = String(dt.getHours()).padStart(2, "0");
    const min = String(dt.getMinutes()).padStart(2, "0");
    const seg = String(dt.getSeconds()).padStart(2, "0");
    return `${dia}/${mes}/${ano} ${hora}:${min}:${seg}`;
  };

  const montarHTMLTipo = (tipo) => {
    const estilo = tipoEstilo[tipo] || {
      cor: "text-secondary",
      icone: "bi-bell",
      texto: tipo
    };
    return `
      <span class="d-inline-flex align-items-center">
        <span class="icon-circle me-2 ${estilo.cor}">
          <i class="bi ${estilo.icone}"></i>
        </span>
        ${estilo.texto}
      </span>
    `;
  };

  const toBase64 = (str) => {
    const bytes = new TextEncoder().encode(str);
    let binary = "";
    for (const b of bytes) {
      binary += String.fromCharCode(b);
    }
    return btoa(binary);
  };
  
  const fromBase64 = (b64) => {
    const binary = atob(b64);
    const bytes = Uint8Array.from(binary.split(""), (ch) => ch.charCodeAt(0));
    return new TextDecoder().decode(bytes);
  };
  

  const converterAlertaParaLinha = (alerta) => {
    const htmlTipo = montarHTMLTipo(alerta.alert_type);

    let htmlMensagem;
    if (alerta.details) {
      const jsonStr = JSON.stringify(alerta);
      const b64 = toBase64(jsonStr);

      htmlMensagem = `
        <span class="alert-link" style="cursor: pointer;"
              data-alert-b64="${b64}"
              onclick="mostrarDetalhesAlertaBase64(this.dataset.alertB64)">
          ${alerta.message}
        </span>
      `;
    } else {
      htmlMensagem = alerta.message;
    }

    const dataTexto = formatarData(alerta.created_at);
    return [ htmlTipo, htmlMensagem, dataTexto ];
  };

  window.mostrarDetalhesAlertaBase64 = (b64) => {
    try {
      const jsonStr = fromBase64(b64);
      const alerta = JSON.parse(jsonStr);
      mostrarDetalhesAlerta(alerta);
    } catch (e) {
      console.error("Falha ao decodificar/parsear alerta:", e);
    }
  };

  const mostrarDetalhesAlerta = (alerta) => {
    const modalEl = document.getElementById("alertModal");
    const modalMessage = document.getElementById("modal-alert-message");
    const modalDetails = document.getElementById("modal-alert-details");

    modalMessage.textContent = alerta.message || "Sem mensagem.";
    modalDetails.textContent = alerta.details || "Nenhum detalhe técnico disponível.";

    const modal = new bootstrap.Modal(modalEl);
    modal.show();

    setTimeout(() => {
      const closeBtn = modalEl.querySelector(".btn-close");
      if (closeBtn) closeBtn.focus();
    }, 200);
  };

  const carregarAlertas = async () => {
    try {
      const url = ultimoCreatedAt
        ? `/api/v1/alerts/list/?since=${encodeURIComponent(ultimoCreatedAt)}`
        : `/api/v1/alerts/list/`;

      const resposta = await fetch(url);
      if (!resposta.ok) throw new Error(`Status ${resposta.status}`);
      const alertas = await resposta.json();

      if (alertas.length > 0) {
        if (!ultimoCreatedAt) {
          dataTable.clear();
          const linhas = alertas.map(converterAlertaParaLinha);
          dataTable.rows.add(linhas).draw();
        } else {
          alertas.forEach((alerta) => {
            const linha = converterAlertaParaLinha(alerta);
            dataTable.row.add(linha).draw(false);
          });
        }
        ultimoCreatedAt = alertas[0].created_at;
      } else if (!ultimoCreatedAt) {
        dataTable.clear().draw();
      }
    } catch (error) {
      console.error("Erro ao carregar alertas:", error);
      if (!ultimoCreatedAt) {
        dataTable.clear();
        dataTable.row.add([
          "",
          `<span class="text-danger">Erro ao carregar alertas.</span>`,
          ""
        ]).draw();
      }
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    dataTable = $("#alert-table").DataTable({
      order: [[2, "desc"]],
      language: {
        url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json",
        emptyTable: "Nenhum alerta encontrado.",
        loadingRecords: "Carregando alertas..."
      },
      paging: false,
      searching: false,
      info: false
    });

    carregarAlertas();
    setInterval(carregarAlertas, 30000);
  });
})();
