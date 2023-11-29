document.addEventListener("DOMContentLoaded", function () {
    const telegramForm2 = document.getElementById("telegramForm");
    const messageInput2 = document.getElementById("messageInput");
    const incomeRows = document.querySelectorAll("tbody tr");

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

        const incomeData = Array.from(incomeRows).map((row) => {
            const stock = row.querySelector("td:nth-child(1)").innerText;
            const name = row.querySelector("td:nth-child(2)").innerText;
            const quantity = row.querySelector("td:nth-child(3)").innerText;
            const totalIncome = row.querySelector("td:nth-child(4)").innerText;
            const incomeDate = row.querySelector("td:nth-child(5)").innerText;
            const numericTotalIncome = parseFloat(totalIncome.replace(/\s/g, '').replace(',', '.'));
            totalAmount += numericTotalIncome;

            return `Приход на ${incomeDate}\nСклад: ${stock}\nНаименование: ${name}\nКоличество: ${quantity}\nСумма: ${totalIncome}`;
        });

        const formattedTotalAmount = totalAmount.toLocaleString('ru-RU');
        const message = `${incomeData.join("\n\n")}\n\nОбщая сумма прихода: ${formattedTotalAmount} UZS`;
        messageInput2.value = message;
        telegramForm2.submit();
    });
});
