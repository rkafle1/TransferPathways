/* Place this tag in the HTML file
   <script src="https://apis.google.com/js/api.js"></script>
*/

// Secret info about Google sheet
// DO NOT PUSH THIS INFO TO GITHUB. Delete before pushing.
const API_KEY = '';
const CLIENT_ID = '';
const SHEET_ID = '';

// Range of the cells you want to read. 
const STARTING_CELL = ''; // e.g. A0
const ENDING_CELL = '';   // e.g. E45

// Initialize the Google Sheets API when the window loads
window.onload = handleClientLoad;

function handleClientLoad() {
    // Load the Google API client library
    gapi.load('client', initClient);
}

function initClient() {
    // Initialize the Google Sheets API client
    gapi.client.init({
        apiKey: API_KEY,
        clientId: CLIENT_ID,
        discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
    }).then(() => {

        // Parse sheet
        parseSheet();

    }).catch(error => {
        console.error('Error initializing API client:', error);
    });
}

// Global variable to store the data
let data;

// Reads and gathers data from the Google sheet
function parseSheet() {
    // Read data from the google sheets
    gapi.client.sheets.spreadsheets.values.get({
        //NOTE: Google sheet has to be public
        spreadsheetId: SHEET_ID,
        range: 'Sheet1!' + STARTING_CELL + ':' + ENDING_CELL
    }).then(response => {
        data = response.result.values;

        /* Loop through the cells of each row
        for (let row = 0; row < data.length; row++) {
            let firstColumn = data[row][0];

            let secondColomn = data[row][1];
            
            let thirdColomn = data[row][2];

            // ... etc ... //
        }
        */

        console.log(data);

    }).catch(error => {
        console.error('Error reading data:', error);
    });
}
