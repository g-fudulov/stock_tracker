document.addEventListener("DOMContentLoaded", getRefreshBtn);

function getRefreshBtn(){
    const refreshBtn  = document.getElementById('request-price');
    refreshBtn.addEventListener('click', handleRefresh);
}

function handleRefresh() {
  // Get the stock symbol from the paragraph with class "symbol"
  const stockSymbolElement = document.querySelector('.symbol.paragraph');
  if (stockSymbolElement) {
    const stockSymbol = stockSymbolElement.textContent.trim();

    // Check if the price is cached
    const cachedData = localStorage.getItem(stockSymbol);

    if (cachedData) {
      const { price, timestamp } = JSON.parse(cachedData);

      // Check if the cached data is still valid (15 seconds duration)
      const currentTime = new Date().getTime();
      if (currentTime - timestamp <= 15 * 1000) {
        // Valid update the field with the cached price
        updatePriceField(price);
      } else {
        // Expired make a new request to fetch the price
        fetchPrice(stockSymbol);
      }
    } else {
      // No cached data, make a new request to fetch the price
      fetchPrice(stockSymbol);
    }
  }
}


function fetchPrice(stockSymbol) {
    const url = `/api/fetch-data/${stockSymbol}`;
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
		let price = data.price
        updatePriceField(price);

        // Cache the fetched price and timestamp in localStorage
        const currentTime = new Date().getTime();
        const cachedData = { price: data.price, timestamp: currentTime };
        localStorage.setItem(stockSymbol, JSON.stringify(cachedData));
      })
      .catch((error) => {
        console.error("Error fetching stock price:", error);
      });
}

function updatePriceField(newPrice){
	const priceField = document.getElementById('id_price');
	priceField.value = newPrice;

}
