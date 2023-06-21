window.onload = handleClientLoad;

let DEBUG = true;

const API_KEY = '';
const CLIENT_ID = '';
const SHEET_ID = '';

function initClient() {
    // Initialize the Google Sheets API client
    gapi.client.init({
        apiKey: API_KEY,
        clientId: CLIENT_ID,
        discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
    }).then(() => {
        parseSheet();
    }).catch(error => {
        console.error('Error initializing API client:', error);
    });
}

function handleClientLoad() {
    // Load the Google API client library
    gapi.load('client', initClient);
}

let formElement = document.getElementById('school-form');
formElement.addEventListener('submit', handleFormSubmit);

let moreInfo = document.getElementById('more-info');
let totalMathSection = document.getElementById('total-math');
let totalScienceSection = document.getElementById('total-science');

let data; // Global variable to store the data
const schoolMap = new Map();

// Reads and gathers data from the Google sheet.
function parseSheet() {
    //Read data from the google sheets
    gapi.client.sheets.spreadsheets.values.get({
        //this id is unique for every sheet (is on the link)
        //NOTE:Google sheet has to be public *** you can also change the range 
        spreadsheetId: SHEET_ID,
        range: 'Sheet1!A1:E82',
    }).then(response => {
        data = response.result.values;

        // array of visited programs to avoid duplicates in map
        let visited = []; 

        // Loop through rows and add data to map starting at row 1 (row 0 is the column titles, so ignore)
        for (let i = 1; i < data.length; i++) {
            // school + program (e.g. UC Irvine + CS B.S.)
            let programName = data[i][0] + ' ' + data[i][1];

            // lower division courses in column 2
            let lower = data[i][2];
            
            // upper division courses in column 3
            let upper = data[i][3];
            
            // If this program is not already a key in the map, make it one
            if (visited.indexOf(programName) == -1) {
                schoolMap.set(programName, {Lower: [], Upper: [], Catalog: {Name: [], Link: []} });
                
                // hyperlinks for catalog and other useful info
                let catalog = data[i][4];
                
                // put all links in the cell in an array. Each link is separated by a new line
                let links = catalog.split("\n");
                
                // Parse links
                for (let i = 0; i < links.length; i++) {
                    // The substring containing the name of the link.
                    let name = links[i].substring(0, links[i].indexOf('http'));

                    // If there is NOT a new line \n at the end of the text, make the end posiotion of the link
                    // the last index of the text.
                    let delimIndex = catalog.indexOf('\n') != -1 ? catalog.indexOf('\n') : catalog.length;

                    // The substring containing the link.
                    let link = links[i].substring(links[i].indexOf('http'), delimIndex);

                    schoolMap.get(programName).Catalog.Name.push(name);
                    schoolMap.get(programName).Catalog.Link.push(link);
                }
                // mark program as visited to avoid duplicating keys
                visited.push(programName);
            }
            // If the values are NOT undefined (an empty cell), add to courselist
            if (lower)
                schoolMap.get(programName).Lower.push(String(lower));
            if (upper)
                schoolMap.get(programName).Upper.push(String(upper));
        }
    }).catch(error => {
        console.error('Error reading data:', error);
    });
}

if (DEBUG)
    console.log(schoolMap);

function parseCellText(cell) {

    let lines = cell.split('<br>');
    let inSublist = false;

    for (let i = 0; i < lines.length; i++) {

        let indx = lines[i].indexOf(":");
        // If there's a colon and the line does NOT start with ^^ or --, add a span for styling
        if (indx !== -1 && !lines[i].startsWith("^^") && !lines[i].startsWith("--")) {
            let courseNum = `<span class="course-number">` + lines[i].substring(0, indx) + `</span>`;
            lines[i] = courseNum + lines[i].substring(indx, lines[i].length);
        }

        // There are 'hints' added in the Google sheet to inform of a style change
        // The hint ^^ means that the text following is a subtitle. Subtitles have unique styling
        if (lines[i].startsWith("^^"))
            lines[i] = '<span class="subject">' + lines[i].substring(2, lines[i].length) + '</span><br>';

        if (inSublist && lines[i].startsWith("--") !== true)
            lines[i] = `<li>` + lines[i] + `</li>`;

        if (!inSublist)
            lines[i] = lines[i] + `<br>`;

        // The hint '--' indicates a sublist (a list within a list).
        if (lines[i].startsWith("--")) {

            // If we're already in a sublist, close it with </ul> and open a new one
            if (inSublist)
                lines[i] = `</ul><span class="bold">` + lines[i].substring(2, lines[i].length) + `</span><ul class="sublist">`;
            else
                lines[i] = `<span class="bold">` + lines[i].substring(2, lines[i].length) + `</span><ul class="sublist">`;

            inSublist = true;
        }
    }
    // Close the <ul> tag if we made sublists in the loop above
    if (inSublist)
        lines[lines.length-1] = lines[lines.length-1] + `</ul>`;

    // Don't join array with commas
    return lines.join("");
}

// Parses the data in the school map
function parseMapData(schoolData, listTag, division) {

    let divisionList = document.getElementById(listTag);
    divisionList.innerHTML = '';
    
    for (let course of schoolData[division]) {
        
        // Highlight OR and AND, and replace special characters like \n with their respective HTML tags
        course = course.replace(/OR/g, '<span class="or">OR</span>');
        course = course.replace(/AND/g, '<span class="and">AND</span>');
        course = course.replace(/\n/g, '<br>');
        
        let li = document.createElement('li');
        li.innerHTML = parseCellText(course);
        
        divisionList.appendChild(li);

        /* if cell has substring 'math' and is NOT in a sentence. 
        There are some cells that have sentence descriptions of required coursework.
        We don't want to include those in the list
        */
        let text = li.innerHTML;
        if ( ( text.includes('Math')  || text.includes('MATH') || text.includes('MAT ') // MAT because Davis uses MAT and not MATH
            || text.includes('Stat')  || text.includes('STAT') )
            && !text.includes('.') ) {
            // Append courses to math section in the HTML file
            let ul = document.createElement('ul');
            ul.innerHTML = text;
            totalMathSection.appendChild(ul);
        }
        // TODO - see why UCI does not mention physics requirement
        if ( ( text.includes('Phy')  || text.includes('PHY') 
            || text.includes('Chem') || text.includes('CHEM'))
            && !text.includes('.')) {
            // Append courses to math section in the HTML
            let ul = document.createElement('ul');
            ul.innerHTML = text;
            totalScienceSection.appendChild(ul);
        }
    }
}

function handleFormSubmit(event) {
    event.preventDefault(); // Prevent form submission

    let selectElement = document.querySelector('#school-select');
    let selectedSchool = selectElement.value; //this is the value form the options tag

    let schoolData = schoolMap.get(selectedSchool);

    // Add selected schools name as the subtitle of the page
    let subTitle = document.getElementById('school-name-subtitle');
    subTitle.innerText = selectedSchool;
    
    // Clear the sections inner HTML
    totalMathSection.innerHTML = '';
    totalScienceSection.innerHTML = '';
    moreInfo.innerHTML = '';

    // Add links to More Info section
    for (let i = 0; i < schoolData.Catalog.Name.length; i++) {
        let moreInfo_p = document.createElement('p');

        let link = `<a href="` + schoolData.Catalog.Link[i] + `">` + "LINK" + `</a>`;
        moreInfo_p.innerHTML = schoolData.Catalog.Name[i] + link;
        moreInfo.appendChild(moreInfo_p);
    }
    
    if (schoolData) {
        let hidden = document.getElementById('main-content');
        hidden.classList.remove('hidden');

        parseMapData(schoolData, 'lower-division', 'Lower');
        parseMapData(schoolData, 'upper-division', 'Upper');

    } else {
        console.log('No data found for the selected school.');
    }
}
