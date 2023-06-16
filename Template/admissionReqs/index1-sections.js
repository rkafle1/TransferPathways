window.onload = handleClientLoad;
let data; // Global variable to store the data

//hashmap to data:
const schoolMap = new Map();

function initClient() {
    // Initialize the Google Sheets API client
    gapi.client.init({
        //i create this apikey on Google console 
        apiKey: 'copy API from goolge docs in here ',
        discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
    }).then(() => {
        readData();
    }).catch(error => {
        console.error('Error initializing API client:', error);
    });
}

function readData() {
    //Read data from the google sheets
    gapi.client.sheets.spreadsheets.values.get({
        //this id is unique for every sheet (is on the link)
        //NOTE:Google sheet has to be public *** change the RANGE as you add more rows/columns 
        spreadsheetId: 'copy and paste the ID from google sheets for index1-sections.js here ',
        range: 'Sheet1!A1:Z80',
    }).then(response => {
        data = response.result.values;

        //JUST ADD THIS 
        let visited = []; // array of visited programs to avoid duplicates in map

        //Display data on console
        // console.log(data);

        for (let i = 1; i < data.length; i++) {
            // school + program (e.g. UC Irvine + CS B.S.)
            let programName = data[i][0] + ' ' + data[i][1]; // THIS HAS TO MATCH THE VALUE IN THE INPUT TAG

            // MATH courses
            let math = data[i][2];

            // CS courses
            let cs_cour = data[i][3];

            // SCIENCE courses
            let science = data[i][4];

            //Required OPTION courses
            let options = data[i][5];

            //Recommended courses 
            let recomm = data[i][6];

            //add GPA Required
            let gpa = data[i][7];

            // if this program is not already a key in the map, make it one
            //Visited take care of the repetitions, if school is already visited will not add to map again 
            if (visited.indexOf(programName) == -1) {
                schoolMap.set(programName, { Math: [], CS: [], Science: [], Options: [], Recommended: [], Gpa: [] });
                visited.push(programName); // mark program as visited
            }

            // if the value is NOT undefined (an empty cell), add to courselist
            if (math)
                schoolMap.get(programName).Math.push(String(math));
            if (cs_cour)
                schoolMap.get(programName).CS.push(String(cs_cour));
            if (science)
                schoolMap.get(programName).Science.push(String(science));
            if (options)
                schoolMap.get(programName).Options.push(String(options));
            if (recomm)
                schoolMap.get(programName).Recommended.push(String(recomm));
            if (gpa)
                schoolMap.get(programName).Gpa.push(String(gpa));
        }
    }).catch(error => {
        console.error('Error reading data:', error);
    });
}

function handleClientLoad() {
    // Load the Google API client library
    gapi.load('client', initClient);
}

function parseMapData(schoolData, listTag, division) {

    let divisionList = document.getElementById(listTag);
    divisionList.innerHTML = '';
    
    // add the titles for each of the sections. If they are no courses in this sections skip. 
    if (listTag == "math-courses" && schoolData.Math.length > 0){
        let mathTitle = document.createElement('h3');
        mathTitle.innerText = 'Math requirements';
        mathTitle.classList.add('math-title-style');
        divisionList.appendChild(mathTitle);
    }
    if(listTag == "science-courses" && schoolData.Science.length > 0){
        let scienceTitle = document.createElement('h3');
        scienceTitle.innerText = 'Science requirements';
        scienceTitle.classList.add('science-title-style');
        divisionList.appendChild(scienceTitle);
    }
    if(listTag == "cse-courses" && schoolData.CS.length > 0){
        let cseTitle = document.createElement('h3');
        cseTitle.innerText = 'CSE requirements';
        cseTitle.classList.add('cs-title-style');
        divisionList.appendChild(cseTitle);
    }
    if(listTag == "option-courses" && schoolData.Options.length > 0){
        let optionsTitle = document.createElement('h3');
        optionsTitle.innerText = 'Other Requirements';
        optionsTitle.classList.add('options-title-style');
        divisionList.appendChild(optionsTitle);
    }

    for (let course of schoolData[division]) {
        let list = document.createElement('li');

        // Highlight OR and AND, and replace special characters
        let replaceOR = course.replace(/OR/g, '<span class="or">OR</span>');
        let replaceAND = replaceOR.replace(/AND/g, '<span class="and">AND</span>');
        let replaceNL = replaceAND.replace(/\n/g, '<br>');

        let text = replaceNL;

        //ADD THIS - make the title bold before the - for each course name 
        //Find the index of the '-' sign
        let dashIndex = text.indexOf('-');
        if (dashIndex !== -1) {
            //Extract the text before the '-' sign
            let beforeDash = text.substring(0, dashIndex);

            // Wrap the text before the '-' sign in <span class="bold">
            let boldText = '<span class="bold">' + beforeDash + '</span>';

            // Replace the text before the '-' sign with the bolded version
            text = boldText + text.substring(dashIndex);
        }


        let subtitleHTML = '';
        // '^^' indicates a subtitle, which should have some unique styling
        let subtitleInx = replaceNL.indexOf('^^');
        // If '^^' is found, wrap the desired subtitle in a <span> element with a class. Class name is tentative
        if (subtitleInx !== -1) {
            let subttl = replaceNL.substring(2, replaceNL.indexOf('<br>'));
            subtitleHTML = '<span class="subject">' + subttl + '</span><br>';
            text = replaceNL.substring(replaceNL.indexOf('<br>') + 4, replaceNL.length);
        }

        // '--' indicates a sublist (a list within the main list). 
        // startSubLists contains the starting indices of every sublist in the cell
        let startSubLists = [...text.matchAll(new RegExp('--', 'gi'))].map(a => a.index);

        if (startSubLists.length > 0) {
            for (let i = 0; i < startSubLists.length; i++) {
                let sublist = document.createElement('ul');
                sublist.classList.add('sublist');

                // sublistData contains the content from the current sublist to the start of the next
                //                                                + 2 to disclude the '--' from the string
                let sublistData = text.substring(startSubLists[i] + 2, startSubLists[i + 1]);

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
                indices.forEach(function (value) {
                    let sublistItem = document.createElement('li');
                    sublistItem.innerHTML = content.substring(prev, value);

                    if (sublistItem.innerHTML == '') return;

                    if (sublistItem.innerHTML.indexOf('--') !== -1) {
                        lastSubListIndex = sublistItem.innerHTML.indexOf('--');
                        return;
                    }
                    sublist.appendChild(sublistItem);
                    prev = value + 4;

                });
                // if loop above does not reach last course
                let sublistItem = document.createElement('li');
                sublistItem.innerHTML = content.substring(prev, content.length);
                if (sublistItem.innerHTML.length > 0)
                    sublist.appendChild(sublistItem);

                list.appendChild(sublist);
            }
        } else {
            list.innerHTML = subtitleHTML + text;
        }
        divisionList.appendChild(list);
    }
}

function handleFormSubmit(event) {
    event.preventDefault(); // Prevent form submission

    var selectElement = document.querySelector('#school-select');
    var selectedSchool = selectElement.value; //this is the value form the options tag

    let schoolData = schoolMap.get(selectedSchool);
    console.log("this is the map at this point  ", schoolMap)

    // Add selected schools name as the subtitle of the page
    let subTitle = document.getElementById('school-name-subtitle');
    subTitle.innerText = selectedSchool;

    if (schoolData) {
        parseMapData(schoolData, 'recommended-courses', 'Recommended');
        parseMapData(schoolData, 'minimum-GPA', 'Gpa');
        parseMapData(schoolData, 'math-courses', 'Math');
        parseMapData(schoolData, 'cse-courses', 'CS');
        parseMapData(schoolData, 'science-courses', 'Science');
        parseMapData(schoolData, 'option-courses', 'Options');
    } else {
        console.log('No data found for the selected school.');
    }
}

//Submission event listener
var formElement = document.getElementById('school-form');
formElement.addEventListener('submit', handleFormSubmit);


  