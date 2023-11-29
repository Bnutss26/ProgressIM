document.addEventListener("DOMContentLoaded", function () {
    const telegramForm = document.getElementById("telegramForm");
    const messageInput = document.getElementById("messageInput");
    const materialDataInputs = document.querySelectorAll("td[data-stock]");

    telegramForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const currentDate = new Date().toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        const itemsData = Array.from(materialDataInputs).map((input) => {
            const stock = input.getAttribute("data-stock");
            const name = input.getAttribute("data-name");
            const unit = input.getAttribute("data-unit");
            let quantity = input.getAttribute("data-quantity");
            quantity = parseInt(quantity);

            let itemDate = `Остаток на ${currentDate}`;
            if (unit === "шт" && quantity <= 5) {
                itemDate += "\nНужно докупить этот материал";
            } else if (unit === "мт" && quantity <= 100) {
                itemDate += "\nНужно докупить этот материал";
            }

            return `${itemDate}\nСклад: ${stock}\nМатериал: ${name} \nКоличество: ${quantity} ${unit}`;
        });

        const message = itemsData.join("\n\n");
        messageInput.value = message;

        telegramForm.submit();
    });
});
