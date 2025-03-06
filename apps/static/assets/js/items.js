const authorizeExecution = async (itemId) => {
  const button = document.getElementById(`authorize-button-${itemId}`);

  if (!button) {
    console.error(`Botão de autorização não encontrado para o item ${itemId}`);
    return;
  }

  // Atualiza o botão visualmente
  button.disabled = true;
  button.textContent = "Aguarde...";

  try {
    const response = await fetch(`/api/v1/items/${itemId}/authorize/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.statusText}`);
    }

    const data = await response.json();
    updateAuthorizeButton(button, data.is_authorized);
    showToast(`Item ${itemId} autorizado com sucesso!`);
  } catch (error) {
    console.error("Erro ao autorizar o item:", error);
    alert("Erro ao autorizar o item. Verifique o console.");
    button.textContent = "Autorizar";
    button.disabled = false;
    showToast(`Erro ao autorizar o item ${itemId}`, 'bg-danger');
  }
};

// ✅ Atualizar visual do botão
const updateAuthorizeButton = (button, isAuthorized) => {
  if (isAuthorized) {
    button.classList.replace("btn-outline-success", "btn-success");
    button.textContent = "Autorizado";
    button.disabled = true;
  } else {
    alert("Falha ao autorizar o item.");
    button.textContent = "Autorizar";
    button.disabled = false;
  }
};

// ✅ Mostrar/Esconder Detalhes do Item
function toggleDetails(itemId) {
  let detailsRow = document.getElementById(`details-${itemId}`);
  detailsRow.style.display =
    detailsRow.style.display === "none" ? "table-row" : "none";
}

function showToast(message) {
  // Cria o elemento HTML do toast
  const toastContainer = document.getElementById("toast-container");
  if (!toastContainer) {
    console.error("Toast container não encontrado!");
    return;
  }
  const toastEl = document.createElement("div");
  toastEl.classList.add(
    "toast",
    "align-items-center",
    "text-white",
    "bg-success",
    "border-0"
  );
  toastEl.setAttribute("role", "alert");
  toastEl.setAttribute("aria-live", "assertive");
  toastEl.setAttribute("aria-atomic", "true");

  // Conteúdo do toast
  toastEl.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    `;

  // Adiciona o toast ao container
  toastContainer.appendChild(toastEl);

  // Inicializa e exibe o toast
  const bsToast = new bootstrap.Toast(toastEl, { delay: 3000 });
  bsToast.show();

  // Remove o toast do DOM após ele desaparecer
  toastEl.addEventListener("hidden.bs.toast", () => {
    toastEl.remove();
  });
}
