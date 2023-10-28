function initialLoad(allBtns) {
  allBtns.forEach((btn) => {
    const stockSymbol = btn.id.replace("btn", "");
    // Check if the stock price is cached in localStorage and if it is still valid
    const cachedData = localStorage.getItem(stockSymbol);

    if (cachedData) {
      const { price, timestamp } = JSON.parse(cachedData);

      // Check if the cached data is still valid (within 10 minutes)
      const currentTime = new Date().getTime();
      if (currentTime - timestamp <= 10 * 60 * 1000) {
        // If the cached data is valid, update the UI with the cached price
        updatePriceElement(stockSymbol, price);
      }
    }
  });
}


document.addEventListener("DOMContentLoaded", function () {
  // Get all the buttons with class "refresh btn"
  const refreshButtons = document.querySelectorAll(".refresh.btn");
  initialLoad(refreshButtons);

  // Add a click event listener to each refresh button
  refreshButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Extract the stock symbol
      const stockSymbol = button.id.replace("btn", "");

      // Check if the stock price is cached in localStorage and if it is still valid
      const cachedData = localStorage.getItem(stockSymbol);

      if (cachedData) {
        const { price, timestamp } = JSON.parse(cachedData);

        // Check if the cached data is still valid (within 10 minutes)
        const currentTime = new Date().getTime();
        if (currentTime - timestamp <= 10 * 60 * 1000) {
          // If the cached data is valid, update the UI with the cached price
          updatePriceElement(stockSymbol, price);
          return;
        }
      }

      // If not cached or expired fetch the price
      fetchStockPrice(stockSymbol);
    });
  });

    function fetchStockPrice(stockSymbol) {
    const url = `/api/fetch-data/${stockSymbol}`;

    // Make a fetch request to the API
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        updatePriceElement(stockSymbol, data.price);

        // Cache the fetched price and timestamp in localStorage
        const currentTime = new Date().getTime();
        const cachedData = { price: data.price, timestamp: currentTime };
        localStorage.setItem(stockSymbol, JSON.stringify(cachedData));
      })
      .catch((error) => {
        console.error("Error fetching stock price:", error);
      });
  }
});

  function updatePriceElement(stockSymbol, price) {
    // Update the stock price in the corresponding <p> element
    const parentPriceElement = document.getElementById(`${stockSymbol} price`);
    const priceElement = parentPriceElement.querySelector('span');
    if (priceElement) {
      if (price === undefined) {
        priceElement.textContent = `error`;
      } else {
        priceElement.textContent = `${price}`;
      }
    }
  }