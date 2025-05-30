let ultimoCreatedAt = null;
let dataTable = null;

const carregarAlertas = async () => {
  try {
    const url = ultimoCreatedAt
      ? `/api/v1/alerts/list/?since=${encodeURIComponent(ultimoCreatedAt)}`
      : `/api/v1/alerts/list/`;

    const resposta = await fetch(url);
    const alertas = await resposta.json();

    const table = document.getElementById("alert-table");
    const tbody = document.getElementById("alert-table-body");
    if (!tbody) return;

    if (alertas.length > 0) {
      // Remove placeholder
      if (
        tbody.children.length === 1 &&
        tbody.children[0].innerText.includes("Carregando")
      ) {
        tbody.innerHTML = "";
      }

      alertas.forEach((alerta) => {
        const tipoEstilo = {
          Informacao: { cor: "text-primary", icone: "bi-info-circle" },
          Erro: { cor: "text-danger", icone: "bi-exclamation-triangle" },
          Sucesso: { cor: "text-success", icone: "bi-check-circle" },
          Alerta: { cor: "text-warning", icone: "bi-exclamation-circle" },
          Debug: { cor: "text-muted", icone: "bi-terminal" },
          Timeout: { cor: "text-dark", icone: "bi-hourglass-split" },
          Validacao: { cor: "text-info", icone: "bi-shield-check" },
          Interrupcao: { cor: "text-dark", icone: "bi-slash-circle" },
        };

        const estilo = tipoEstilo[alerta.alert_type] || {
          cor: "text-secondary",
          icone: "bi-bell",
        };

        const row = document.createElement("tr");

        // Coluna: Tipo
        const tipoTd = document.createElement("td");
        tipoTd.innerHTML = `
          <span class="d-inline-flex align-items-center">
            <span class="icon-circle me-2 ${estilo.cor}">
              <i class="bi ${estilo.icone}"></i>
            </span>
            ${alerta.alert_type}
          </span>
        `;

        // Coluna: Mensagem
        const mensagemTd = document.createElement("td");
        if (alerta.details) {
          const span = document.createElement("span");
          span.className = "alert-link";
          span.textContent = alerta.message;
          span.style.cursor = "pointer";
          span.dataset.alert = JSON.stringify(alerta);
          span.onclick = () => {
            mostrarDetalhesAlerta(JSON.parse(span.dataset.alert));
          };
          mensagemTd.appendChild(span);
        } else {
          mensagemTd.textContent = alerta.message;
        }

        // Coluna: Data
        const dataTd = document.createElement("td");
        const createdAt = new Date(alerta.created_at);
        dataTd.setAttribute("data-order", createdAt.getTime());
        dataTd.textContent = createdAt.toLocaleString();

        // Monta a linha
        row.appendChild(tipoTd);
        row.appendChild(mensagemTd);
        row.appendChild(dataTd);

        // Adiciona à tabela
        tbody.prepend(row);

        if (dataTable) {
          dataTable.row.add(row).draw(false);
        }
      });

      // Atualiza timestamp
      ultimoCreatedAt = alertas[0].created_at;
    } else if (tbody.children.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="text-muted">Nenhum alerta encontrado.</td></tr>`;
    }
  } catch (error) {
    console.error("Erro ao carregar alertas:", error);
    const tbody = document.getElementById("alert-table-body");
    if (tbody && tbody.children.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="text-danger">Erro ao carregar alertas.</td></tr>`;
    }
  }
};

const mostrarDetalhesAlerta = (alerta) => {
  const modalEl = document.getElementById("alertModal");
  const modalMessage = document.getElementById("modal-alert-message");
  const modalDetails = document.getElementById("modal-alert-details");

  modalMessage.textContent = alerta.message || "Sem mensagem.";
  modalDetails.textContent =
    alerta.details || "Nenhum detalhe técnico disponível.";

  modalEl.setAttribute("aria-hidden", "false");
  modalEl.style.display = "block";

  const modal = new bootstrap.Modal(modalEl);
  modal.show();

  setTimeout(() => {
    const closeBtn = modalEl.querySelector(".btn-close");
    if (closeBtn) closeBtn.focus();
  }, 200);
};

document.addEventListener("DOMContentLoaded", () => {
  carregarAlertas();
  setInterval(carregarAlertas, 30000);

  setTimeout(() => {
    dataTable = $("#alert-table").DataTable({
      order: [[2, "desc"]],
      language: {
        url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json",
      },
    });
  }, 500);
});
