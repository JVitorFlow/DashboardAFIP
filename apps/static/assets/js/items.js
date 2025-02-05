const authorizeExecution = async (itemId) => {
    try {
        const response = await fetch(`/api/v1/items/${itemId}/authorize/`, {  // URL relativa
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            alert("Falha ao autorizar o item.");
            return;
        }

        const data = await response.json();
        const { is_authorized } = data;

        if (is_authorized) {
            const button = document.getElementById(`authorize-button-${itemId}`);
            button.classList.replace('btn-outline-success', 'btn-success');
            button.textContent = "Autorizado";
            button.disabled = true;
        } else {
            alert("Falha ao autorizar o item.");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao autorizar o item.");
    }
};
