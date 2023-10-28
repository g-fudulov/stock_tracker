function addEvents() {
    const calcBtns = document.querySelectorAll(".pnl.btn");
    calcBtns.forEach((button) => {
        button.addEventListener('click', handleRefresh);
    })
}

function handleRefresh(){
    let stockSymbol = this.id.replace(' pnl-btn', "")
    const avgPrice = parseFloat(document.getElementById(`${stockSymbol} avg_price`).textContent.replace('Average Price: $', ""));
    const elementCurrPrice = document.querySelector(`.${stockSymbol}.current-price`);

    if (elementCurrPrice.textContent) {
        const currPrice = parseFloat(elementCurrPrice.textContent);
        calcPnl(avgPrice, currPrice, stockSymbol);
    } else {
        const refreshPriceBtn = document.getElementById(`${stockSymbol}btn`)
        // Fetch again
        refreshPriceBtn.click()
        // Calc pnl
        this.click()
        this.click()
    }
}

function calcPnl(avgPrice, currPrice, stockSymbol) {
    const elementPnl = document.querySelector(`.${stockSymbol}.current-pnl`);
    const elementShares = document.getElementById(`${stockSymbol} shares`);
    if (elementPnl && elementShares) {
        // Calculate pnl
        const pnl = (((currPrice - avgPrice) / avgPrice) * 100).toFixed(2);
        const dollarPnl = (currPrice - avgPrice) * parseFloat(elementShares.textContent.replace('Shares: ', ''))

        if (isNaN(pnl) || isNaN(dollarPnl)) {
            elementPnl.textContent = 'error';
            elementPnl.style.color = '#fa6464';
            return;
        }

        elementPnl.textContent = `${pnl}% | $${dollarPnl.toFixed(2)}`;
        // Set color
        if (pnl > 0) {
            elementPnl.style.color = '#2ed832'; // Profit (green)
        } else if (pnl < 0) {
            elementPnl.style.color = '#fa6464'; // Loss (red)
        } else {
            elementPnl.style.color = '#ffffff'; // Neutral (black)
        }
    }
}

document.addEventListener("DOMContentLoaded", addEvents);
