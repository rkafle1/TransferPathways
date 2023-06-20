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

            // links to catalog and other useful info
            let catalog = data[i][4];

            // if this program is not already a key in the map, make it one
            if (visited.indexOf(programName) == -1) {
                schoolMap.set(programName, {Lower: [], Upper: [], Catalog: {Name: [], Link: []} });

                // put all links in the cell in an array. Each link is separated by a new line
                let links = catalog.split("\n");
                
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
                // mark program as visited to avoid duplicate keys
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

function parseSubList(sublistData, list, subtitleHTML) {
            let sublist = document.createElement('ul');
            sublist.classList.add('sublist');
            
            // To change the style of the 'title' of the sublist, get the first line break <br> in the
            // sublist data, and wrap the 'title' in a <span>
            let br = sublistData.indexOf('<br>') + 4;
            let ttl = '<span class="bold">' + sublistData.substring(0, br) + '</span>';
            // Append to the HTML of the list. If there was a '^^' found earlier, append the subtitle as well as
            // the title of the sublist. Set subtitleHTML to '' so not to append the subtitle more than once
            list.innerHTML += subtitleHTML + ttl;
            subtitleHTML = '';
            
            // Content of sublist data without the title. This will be put into <li> tags
            let content = sublistData.substring(br, sublistData.length);
            
            // Find all the line breaks in the cell. Each line of data will have its own <li> element
            let indices = [...content.matchAll(new RegExp('<br>', 'gi'))].map(a => a.index);
        
            let prev = 0;
            indices.forEach(function(index) {
                let sublistItem = document.createElement('li');
                sublistItem.innerHTML = content.substring(prev, index);
                
                // If the current line of text is supposed to be a sublist
                if (sublistItem.innerHTML.indexOf('--') !== -1) return;
                // If nothing was read
                if (sublistItem.innerHTML == '') return;
                sublist.appendChild(sublistItem);
                prev = index + 4; // +4 since '<br>' is 4 characters and we don't want to start at <br>
            });
            // If loop above does not reach last course
            let sublistItem = document.createElement('li');
            sublistItem.innerHTML = content.substring(prev, content.length);
            if (sublistItem.innerHTML.length > 0)
                sublist.appendChild(sublistItem);
            list.appendChild(sublist);
}

// TODO - split courses by new line like how we did for Catalog links.

// Parses the data in the school map
function parseMapData(schoolData, listTag, division) {

    let divisionList = document.getElementById(listTag);
    divisionList.innerHTML = '';

    for (let course of schoolData[division]) {
        let list = document.createElement('li');
        
        // Highlight OR and AND, and replace special characters like \n with their respective HTML tags
        let replaceOR = course.replace(/OR/g, '<span class="or">OR</span>');
        let replaceAND = replaceOR.replace(/AND/g, '<span class="and">AND</span>');
        let replaceNL = replaceAND.replace(/\n/g, '<br>');
        
        // this is the text of the content of the cell after the above changes
        let text = replaceNL;
        
        let subtitleHTML = '';

        // There are 'hints' added in the Google sheet to inform of a style change
        // The hint ^^ means that the text following is a subtitle. Subtitles have unique styling
        let subtitleIndex = replaceNL.indexOf('^^');

        // If '^^' is found, wrap the subtitle in a <span> element with the class "subject".
        if (subtitleIndex !== -1) {
            // It will read up until the first new line. In the Google sheet, the subtitles are on their own line
            let subttl = replaceNL.substring(2, replaceNL.indexOf('<br>'));

            // Put the subtitle in a span tag with the class "subject". Add a line break at the end
            subtitleHTML = '<span class="subject">' + subttl + '</span><br>';

            // Add this change to the text. (i don't like how strings in JavaScript are immutable)
            text = replaceNL.substring(replaceNL.indexOf('<br>') + 4, replaceNL.length);
        }

        /* if cell has substring 'math' and is NOT in a sentence. 
          There are some cells that have sentence descriptions of required coursework.
          We don't want to include those in the list
        */
        if ( ( text.includes('Math')  || text.includes('MATH') // MAT because Davis uses MAT and not MATH
            || text.includes('Stat')  || text.includes('STAT') )
            && !text.includes('.') ) {
            // Append courses to math section in the HTML file
            let ul = document.createElement('ul');
            ul.innerHTML = `<li>` + text + `</li>`;
            totalMathSection.appendChild(ul);
        }
        // TODO - see why UCI does not mention physics requirement
        if ( ( text.includes('Phy')  || text.includes('PHY') 
            || text.includes('Chem') || text.includes('CHEM'))
            && !text.includes('.')) {
            // Append courses to math section in the HTML
            let ul = document.createElement('ul');
            ul.innerHTML = `<li>` + text + `</li>`;
            totalScienceSection.appendChild(ul);
        }
        
        // The hint '--' indicates a sublist (a list within a list).
        // startSubLists contains the starting indices of every sublist in the cell
        let startSubLists = [...text.matchAll(new RegExp('--', 'gi'))].map(a => a.index);

        // If there are substring hints in the cell
        if (startSubLists.length > 0) {
            for (let i = 0; i < startSubLists.length; i++) {
                // sublistData contains the content from the current sublist to the start of the next
                //                                                + 2 to disclude the '--' from the string
                let sublistData = text.substring(startSubLists[i] + 2, startSubLists[i + 1]);
                parseSubList(sublistData, list, subtitleHTML);
            }
        }
        else
            list.innerHTML = subtitleHTML + text;

        divisionList.appendChild(list);
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
