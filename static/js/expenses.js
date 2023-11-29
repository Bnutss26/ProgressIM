document.addEventListener("DOMContentLoaded", function () {
    const telegramForm2 = document.getElementById("telegramForm");
    const messageInput2 = document.getElementById("messageInput");
    const expenseRows = document.querySelectorAll("tbody tr");
    telegramForm2.addEventListener("submit", function (e) {
        e.preventDefault();
        let totalAmount = 0;
        let currentDate = '';
        let expensePrefix = '';
        const expensesData = Array.from(expenseRows).map((row) => {
            const stock = row.querySelector(".stock") ? row.querySelector(".stock").innerText : '';
            const name = row.querySelector(".name") ? row.querySelector(".name").innerText : '';
            const quantity = row.querySelector(".quantity") ? row.querySelector(".quantity").innerText : '';
            const unit = row.querySelector(".unit") ? row.querySelector(".unit").innerText : '';
            const totalCost = row.querySelector(".total-cost") ? row.querySelector(".total-cost").innerText : '';
            const expensesDate = row.querySelector(".expenses-date") ? row.querySelector(".expenses-date").innerText : '';
            if (totalCost !== '') {
                const numericTotalCost = parseFloat(totalCost.replace(/\s/g, '').replace(',', '.'));
                totalAmount += numericTotalCost;
            }
            if (currentDate === '') {
                currentDate = expensesDate;
                expensePrefix = `Расход на ${expensesDate}\n`;
            }
            return `${expensePrefix}Склад: ${stock}\nНаименование: ${name}\nКоличество: ${quantity} ${unit}\nСумма: ${totalCost}`;
        });
        const formattedTotalAmount = totalAmount.toLocaleString('ru-RU');
        const message = `\n${expensesData.join("\n\n")}\n\nОбщая сумма расхода: ${formattedTotalAmount} UZS`;
        messageInput2.value = message;
        telegramForm2.submit();
    });
});
