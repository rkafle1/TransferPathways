
const API_KEY = 'AIzaSyBgdJG0I6zU8elZzB7Bsl79Jhyls7fsT9U';
const CLIENT_ID = '964029012495-khufmlfdkqe6qd5c6snnql5h1v22euo4.apps.googleusercontent.com';
const SHEET_ID = '1_s_TiZGaR-WHfAV5KpKr4BJq0r61UTCsEcCQJuy_OSk';

let data; // Global variable to store the data
const schoolMap = new Map(); // Holds the data for each school

let moreInfo = document.getElementById('more-info');
let totalMathSection = document.getElementById('total-math');
let totalScienceSection = document.getElementById('total-science');

window.onload = handleClientLoad;

let DEBUG = true;

if (DEBUG)
    console.log(schoolMap);
    
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
        parseSheet();

    }).catch(error => {
        console.error('Error initializing API client:', error);
    });
}

// Reads and gathers data from the Google sheet. Puts the data in a map
function parseSheet() {

    //Read data from the google sheets
    gapi.client.sheets.spreadsheets.values.get({
        //this id is unique for every sheet (is on the link)
        //NOTE:Google sheet has to be public *** you can also change the range 
        spreadsheetId: SHEET_ID,
        range: 'Sheet1!A2:E401',
    }).then(response => {
        data = response.result.values;

        // array of visited programs to avoid duplicates in map
        let visited = [];

        // Loop through rows and add data to map
        for (let i = 0; i < data.length; i++) {
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
                
                // put all links in the cell in an array. Each link is separated by a new line \n
                let links = catalog.split("\n");
                
                // Parse links
                for (let i = 0; i < links.length; i++) {
                    // The substring containing the name of the link.
                    let name = links[i].substring(0, links[i].indexOf('http'));

                    // If there is NOT a new line \n at the end of the text, make the end posiotion of the link
                    // the last index of the text.
                    let delimIndex = links[i].indexOf('\n') != -1 ? links[i].indexOf('\n') : links[i].length;

                    // The substring containing the link.
                    let link = links[i].substring(links[i].indexOf('http'), delimIndex);

                    schoolMap.get(programName).Catalog.Name.push(name);
                    schoolMap.get(programName).Catalog.Link.push(link);
                }
                // mark program as visited to avoid duplicating keys
                visited.push(programName);
            }
            // If the values are NOT undefined (an empty cell), add to courselist
            if (lower) {
                schoolMap.get(programName).Lower.push(String(lower));
            }
            if (upper) {
                schoolMap.get(programName).Upper.push(String(upper));
            }
        }

    }).catch(error => {
        console.error('Error reading data:', error);
    });
}

// Parces and handles the text from each individual cell in the Google sheet
function parseCell(cell) {

    let inSublist = false;

    // Split the cell by line breal <br> and put each line into array
    let lines = cell.split('<br>');
    // Parse each line of the cell
    for (let i = 0; i < lines.length; i++) {

        // There are 'hints' added in the Google sheet to inform of a style change
        // The hint ^^ means that the text following is a subtitle. Subtitles have unique styling
        // The hint -- indicates a sublist (a list within the main list).
        // The hint ** means the line needs to be bold
        let bold = lines[i].startsWith("**");
        let sublist = lines[i].startsWith("--");
        let title = lines[i].startsWith("^^");

        let indx = lines[i].indexOf(":");
        // If there's a colon and the line does NOT start with ^^ or --, add a span for styling
        if (indx !== -1 && !title && !sublist && !bold) {
            let courseNum = `<span class="course-number">` + lines[i].substring(0, indx + 1) + `</span>`;
            lines[i] = courseNum + lines[i].substring(indx + 1, lines[i].length);
        }

        if (bold)
            lines[i] = '<span class="bold">' + lines[i].substring(2, lines[i].length) + '</span>';

        if (title) {
            lines[i] = '<span class="subject">' + lines[i].substring(2, lines[i].length) + '</span>';
            if (inSublist) {
                // close sublist and add line break
                lines[i] = `</ul><br>` + lines[i];
                inSublist = false;
            }
        }

        if (inSublist && sublist === false)
            lines[i] = `<li>` + lines[i] + `</li>`;

        if (!inSublist)
            lines[i] = lines[i] + `<br>`;

        if (sublist) {
            // If we're already in a sublist, close it with </ul> and open a new one
            if (inSublist)
                lines[i] = `</ul><br><span class="bold">` + lines[i].substring(2, lines[i].length) + `</span><ul class="sublist">`;
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
        course = course.replace(/OR /g, '<span class="or">OR</span> ');    // added space so words with OR are not highlighted (e.g. CORE) *find better way
        course = course.replace(/AND /g, '<span class="and">AND</span> '); // added space so words with AND are not highlighted (e.g. LAND)
        course = course.replace(/\n/g, '<br>');
        
        let li = document.createElement('li');

        li.innerHTML = parseCell(course);
        
        divisionList.appendChild(li);

        // If cell has substring 'math' and is NOT in a sentence. 
        // There are some cells that have sentence descriptions of required coursework.
        // We don't want to include those in the list
        
        let text = li.innerHTML;
        if ( ( text.includes('Math')  || text.includes('MATH') || text.includes('MAT ') // MAT because Davis uses MAT and not MATH
            || text.includes('Stat')  || text.includes('STAT ') || text.includes('STATS '))
            && !text.includes('.') ) {
            // Append courses to math section in the HTML file
            let item = document.createElement('li');
            item.innerHTML = text;
            totalMathSection.appendChild(item);
        }
        else if ( ( text.includes('Phy ')  || text.includes('PHY ') || text.includes('Physics') 
            || text.includes('Chem') || text.includes('CHEM ') || text.includes('Biol') || text.includes('BIO'))
            && !text.includes('.')) {
            // Append courses to math section in the HTML
            let item = document.createElement('li');
            item.innerHTML = text;
            totalScienceSection.appendChild(item);
        }
    }
}

let formElement = document.getElementById('school-form');
formElement.addEventListener('submit', handleFormSubmit);

function handleFormSubmit(event) {
    event.preventDefault(); // Prevent form submission

    let selectElement = document.querySelector('#school-select');
    let selectedSchool = selectElement.value; //this is the value from the options tag

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

        let link = `<a target="_blank" rel="noopener noreferrer" href="` + schoolData.Catalog.Link[i] + `">` + "LINK" + `</a>`;
        moreInfo_p.innerHTML = schoolData.Catalog.Name[i] + link;
        moreInfo.appendChild(moreInfo_p);
    }
    
    if (schoolData) {
        let hidden = document.getElementById('main-content');
        hidden.classList.remove('hidden');

        //let main = document.getElementById('grad-main');
        //main.style.background = 'none';

        let lowerSummary = document.getElementById('lower-div-summary');
        let upperSummary = document.getElementById('upper-div-summary');

        // Some schools do not give explicit Lower/Upper div course details.
        // Change the names of the drop down menus
        if (selectedSchool === 'Cal Poly Pomona CS B.S.') {
            lowerSummary.innerText = 'Major Required';
            upperSummary.innerText = 'Major Electives';
        }
        else if (selectedSchool === 'CSU Monterey Bay CS B.S.') {
            lowerSummary.innerText = 'Required Courses';
            upperSummary.innerText = 'Concentrations';
        }
        else if (selectedSchool === 'Cal Poly San Luis Obispo CS B.S.') {
            let note = `<p>This tool could only display certain information for requirements of the CS major at this school.<br>
                        For more information on articulation requirements and what courses to take to be a competitive applicant,
                        visit the ADMISSIONS page on this website.<br><br>
                        It is imperative that you review the resources below for more information about this major.</p>`
            moreInfo.innerHTML = note + moreInfo.innerHTML;
            lowerSummary.innerText = 'Major Courses';
            upperSummary.innerText = 'Support Courses';
        }
        else {
            lowerSummary.innerText = 'Lower Division';
            upperSummary.innerText = 'Upper Division';
        }

        parseMapData(schoolData, 'lower-division', 'Lower');
        parseMapData(schoolData, 'upper-division', 'Upper');

        if (totalMathSection.innerHTML === '') {
            let item = document.createElement('li');
            item.innerHTML = "none";
            totalMathSection.appendChild(item);
        }
        if (totalScienceSection.innerHTML === '') {
            let item = document.createElement('li');
            item.innerHTML = "none";
            totalScienceSection.appendChild(item);
        }

    } else {
        console.error('No data found for the selected school.');
    }
}