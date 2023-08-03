import React, { useState, useEffect } from 'react';
import './stock.css';
import { Chart, LineController, CategoryScale, LinearScale, PointElement, LineElement, Tooltip } from 'chart.js';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowAltCircleUp, faArrowAltCircleDown, faArrowsAltH } from '@fortawesome/free-solid-svg-icons';
import jsonData from './stocks_symb.json';

function StockSearch() {
  // Setting initial stock input/info to null/clear
  const [stockInput, setStockInput] = useState(''); // State to hold user input for stock symbol
  const [stockInfo, setStockInfo] = useState(null); // State to hold retrieved stock information
  const [newsArticles, setNewsArticles] = useState([]); // State to hold retrieved news articles
  const [chartData, setChartData] = useState(null); // State to hold retrieved chart data
  const apiKey = process.env.STOCK_API_KEY;  //API Key for Alpha Vantage data

  useEffect(() => {
    searchStock(); // Call searchStock function when the component mounts
  }, []);

  useEffect(() => {
    if (chartData) {
      createChart();
    }
  }, [chartData]);

  const handleInputChange = (event) => {
    setStockInput(event.target.value); // Update stock input state with user's input
  };

  const searchStock = () => {
    // Clear previous stock information
    setStockInfo(null);
    setNewsArticles([]);
    setChartData(null);

    // Fetch stock data
    fetchStockData(stockInput)
      .then((data) => {
        if (Object.keys(data['Global Quote']).length !== 0) {
          setStockInfo(data); // Update stock information state with retrieved data
        } else {
          // Handle case when no data is returned
          setStockInfo({ error: 'No data found for the stock symbol. Try using the company symbol instead of the company name.' });
        }
      })
      .catch((error) => {
        setStockInfo({ error: 'Search for a valid stock symbol to receive filtered news and stock analytics.' });
        console.error('Error:', error);
      });

    // Fetch news articles
    fetchNewsArticles(stockInput)
      .then((data) => {
        setNewsArticles(data.feed); // Update news articles state with retrieved data
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    // Fetch chart data
    fetchChartData(stockInput)
      .then((data) => {
        setChartData(data["Weekly Adjusted Time Series"]); // Update chart data state with retrieved data
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const fetchStockData = (stockSymbol) => {
    // fetch stock company data from alphavantage api
    const apiUrl = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${stockSymbol}&apikey=${apiKey}`;

    return fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      });
  };

  const fetchChartData = (stockSymbol) => {
    //fetch stock price data from alphavantage time series API
    const apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=${stockSymbol}&apikey=${apiKey}`;

    return fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      });
  };

  const fetchNewsArticles = (stockSymbol) => {
    // fetch news feed for searched stock from alphavantage with sentiment analysis
    const apiUrl = `https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=${stockSymbol}&apikey=${apiKey}`;

    return fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      });
  };

  const createChart = () => {
    const dates = Object.keys(chartData).reverse(); // Get the dates from chart data in reverse order
    const prices = dates.map((date) => parseFloat(chartData[date]['4. close'])); // Get the closing prices corresponding to the dates

    const ctx = document.getElementById('price-chart').getContext('2d');
    Chart.register(LineController, CategoryScale, LinearScale, PointElement, LineElement, Tooltip);

    //create line chart with stock price over time
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [{
          label: 'Stock Prices',
          data: prices,
          borderColor: 'blue',
          backgroundColor: 'rgba(0, 0, 255, 0.1)',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  };

  return (
    <div className="container">
      <h1>WallStreetBets Dashboard</h1>

      <form className="search-form">
        <input
          type="text"
          id="stock-input"
          placeholder="Enter a stock symbol"
          value={stockInput}
          onChange={handleInputChange}
        />
        <button type="button" onClick={searchStock}>Search</button>
      </form>

      {/* Display stock information */}
      {stockInfo && stockInfo['error'] ? (
        <div className="stock-info">
          <p>{stockInfo.error}</p>
        </div>
      ) : stockInfo && stockInfo['Global Quote'] ? (
        <div className="stock-info">
          {/* Use jsonData to lookup symbol name based on retrieved symbol */}
          <h2>{jsonData[stockInfo['Global Quote']['01. symbol']]}</h2>
          <p>Price: {stockInfo['Global Quote']['05. price']}</p>
          <p>As of: {stockInfo['Global Quote']['07. latest trading day']}</p>
        </div>
      ) : null}

      {/* Display price chart */}
      {chartData && (
        <div className="chart-container">
          <canvas id="price-chart"></canvas>
        </div>
      )}

      {/* Display news articles */}
      {newsArticles && (
  <div id="news-articles">
    <h2>News Feed</h2>

    {/* Legend for Sentiment Label*/}
    <div className="legend">
      <span className="legend-item">
        <FontAwesomeIcon icon={faArrowAltCircleUp} color="green" size="lg" />
        <span className="legend-text">Positive</span>
     </span>
      <span className="legend-item">
        <FontAwesomeIcon icon={faArrowAltCircleDown} color="red" size="lg" />
        <span className="legend-text">Negative</span>
      </span>
      <span className="legend-item">
        <FontAwesomeIcon icon={faArrowsAltH} color="gray" size="lg" />
        <span className="legend-text">Neutral</span>
      </span>
    </div>
    {newsArticles.map((article) => {
      let arrowIcon = null;
      let arrowColor = null;

      if (article['overall_sentiment_score'] >= 0.15) {     //Green Arrow if news is positive
        arrowIcon = faArrowAltCircleUp;
        arrowColor = 'green';
      } else if (article['overall_sentiment_score'] <= 0.00) {  //Red Arrow if news is negative
        arrowIcon = faArrowAltCircleDown;
        arrowColor = 'red';
      } else {
        arrowIcon = faArrowsAltH;
        arrowColor = 'gray';     //Gray Arrow if news is neutral
      }

      return (
        <div key={article['title']} className="news-article">
          <h3>
            <FontAwesomeIcon icon={arrowIcon} color={arrowColor} size="lg" /> {article['title']}
          </h3>
          <p>{article['summary']}</p>
          <p>Source: <a href={article['url']} target="_blank">{article['authors'][0]}</a></p>
        </div>
      );
    })}
  </div>
)}

    </div>
  );
}

export default StockSearch;
