const telegramForm2 = document.getElementById("telegramForm");
const messageInput2 = document.getElementById("messageInput");
const expenseRows = document.querySelectorAll("tbody tr");
const drop_btn = document.querySelector(".drop_btn");
telegramForm2.addEventListener("submit", function (e) {
    e.preventDefault();
    const currentDate = new Date().toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
    });
    let totalAmount = 0;
    const expensesData = Array.from(expenseRows).map((row) => {
        const stock = row.querySelector("td:nth-child(1)").innerText;
        const name = row.querySelector("td:nth-child(2)").innerText;
        const quantity = row.querySelector("td:nth-child(3)").innerText;
        const totalCost = row.querySelector("td:nth-child(4)").innerText;
        const debtorName = row.querySelector("td:nth-last-child(2)").innerText;
        const expensesDate = row.querySelector("td:nth-child(6)").innerText;
        const numericTotalCost = parseFloat(totalCost.replace(/\s/g, '').replace(',', '.'));
        totalAmount += numericTotalCost;
        return `Долг на ${expensesDate}\nСклад: ${stock}\nНаименование: ${name}\nКоличество: ${quantity}\nСумма: ${totalCost}\nДолжник: ${debtorName}`;
    });
    const formattedTotalAmount = totalAmount.toLocaleString('ru-RU');
    const message = `\n${expensesData.join("\n\n")}\n\nОбщая сумма долгов: ${formattedTotalAmount} UZS`;
    messageInput2.value = message;
    telegramForm2.submit();
});