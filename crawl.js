const puppeteer = require("puppeteer");
const axios = require('axios');
const fs = require('fs');

const run = async () => {
  try {
    // Fetch historical data for the Fear and Greed Index
    const fearAndGreedData = await fetchFearAndGreedData();

    // Remove duplicates from Fear and Greed Index data
    const uniqueFearAndGreedData = removeDuplicates(fearAndGreedData.csvData);

    // Write the unique Fear and Greed Index data to CSV file
    fs.writeFileSync('fear_and_greed_data.csv', uniqueFearAndGreedData);

    // Fetch historical data for the S&P 500 index
    const sp500Data = await fetchSAndP500Data(fearAndGreedData.firstDate, fearAndGreedData.lastDate);

    // Write the S&P 500 index data to CSV file
    fs.writeFileSync('sp500_data.csv', sp500Data);

    console.log('Data fetched and saved successfully');
  } catch (error) {
    console.error('Error fetching data:', error.message);
  }
};

const removeDuplicates = (csvData) => {
  // Split CSV data into rows
  const rows = csvData.split('\n');

  // Create a Set to store unique rows
  const uniqueRows = new Set();

  // Iterate over each row and add it to the Set
  for (const row of rows) {
    // Skip empty rows
    if (row.trim() !== '') {
      uniqueRows.add(row);
    }
  }

  // Join unique rows back into CSV format
  return Array.from(uniqueRows).join('\n');
};

const fetchFearAndGreedData = async () => {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage();
  await page.goto('https://production.dataviz.cnn.io/index/fearandgreed/graphdata');
  const selector = 'pre';
  await page.waitForSelector(selector);

  let data = await page.$eval(selector, (element) => element.textContent);
  let data_json = JSON.parse(data);

  let data_array = data_json.fear_and_greed_historical.data;
  
  const csvData = [
    [
      "datetime",
      "index_value",
      "rating"
    ],
    ...data_array.map(item => [
      timestamptodatestr(item.x),
      item.y,
      item.rating
    ])
  ]
  .map(e => e.join(","))
  .join("\n");

  browser.close();

  // Extract first and last dates from the Fear and Greed Index data
  const firstDate = data_array[0].x / 1000;
  const lastDate = data_array[data_array.length - 1].x / 1000;

  return { csvData, firstDate, lastDate };
};

const fetchSAndP500Data = async (startDate, endDate) => {
  const response = await axios.get(`https://query1.finance.yahoo.com/v7/finance/download/%5EGSPC?period1=${startDate}&period2=${endDate}&interval=1d&events=history`);
  console.log('start date : ' + startDate + ' end date : ' + endDate);
        
  return response.data;
};

const timestamptodatestr = (ts) => {
  const d = new Date(ts);
  let datestr = d.toISOString().slice(0, 10);
  return datestr;
};

run();
