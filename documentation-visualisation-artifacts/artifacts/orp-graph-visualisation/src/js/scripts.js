var cy_basic_search, cy_filtered, cy_stale, cy_reconfirmed;

// Styles
var styles = {
    name: 'cose',
    idealEdgeLength: 100,
    nodeOverlap: 20,
    refresh: 20,
    fit: true,
    padding: 30,
    randomize: false,
    componentSpacing: 100,
    nodeRepulsion: 400000,
    edgeElasticity: 100,
    nestingFactor: 5,
    gravity: 80,
    numIter: 1000,
    initialTemp: 200,
    coolingFactor: 0.95,
    minTemp: 1.0,
    wheelSensitivity: 0
}

// Basic Search

initBasicSearch();

function initBasicSearch() {
    Promise.all([
        fetch('./data/style.json')
            .then(function (res) {
                return res.json()
            }),
        fetch('./data/basic_search.json')
            .then(function (res) {
                return res.json()
            })
    ]).then(function (dataArray) {
        cy_basic_search = window.cy = cytoscape({
            container: document.getElementById('basic_search'),
            layout: styles,
            style: dataArray[0],
            elements: dataArray[1].response
        });
        cy_basic_search.minZoom(2);
        cy_basic_search.maxZoom(10);
    });
}

document.getElementById("reset_basic_search").addEventListener("click", resetBasicSearch);
function resetBasicSearch() {
    cy_basic_search.destroy();
    initBasicSearch();
}

// Filtered

initFiltered();

function initFiltered() {
    Promise.all([
        fetch('./data/style.json')
            .then(function (res) {
                return res.json()
            }),
        fetch('./data/filtered.json')
            .then(function (res) {
                return res.json()
            })
    ]).then(function (dataArray) {
        cy_filtered = window.cy = cytoscape({
            container: document.getElementById('filtered'),
            layout: styles,
            style: dataArray[0],
            elements: dataArray[1].response
        });
        cy_filtered.minZoom(2);
        cy_filtered.maxZoom(10);
    });
}

document.getElementById("reset_filtered").addEventListener("click", resetFiltered);
function resetFiltered() {
    cy_filtered.destroy();
    initFiltered();
}


// Stale

initStale();

function initStale() {
    Promise.all([
        fetch('./data/style.json')
            .then(function (res) {
                return res.json()
            }),
        fetch('./data/stale.json')
            .then(function (res) {
                return res.json()
            })
    ]).then(function (dataArray) {
        cy_stale = window.cy = cytoscape({
            container: document.getElementById('stale'),
            layout: styles,
            style: dataArray[0],
            elements: dataArray[1].response
        });
        cy_stale.minZoom(2);
        cy_stale.maxZoom(10);
    });
}

document.getElementById("reset_stale").addEventListener("click", resetStale);
function resetStale() {
    cy_stale.destroy();
    initStale();
}


// Reconfirmed
initReconfirmed();

function initReconfirmed() {
    Promise.all([
        fetch('./data/style.json')
            .then(function (res) {
                return res.json()
            }),
        fetch('./data/reconfirmed.json')
            .then(function (res) {
                return res.json()
            })
    ]).then(function (dataArray) {
        cy_reconfirmed = window.cy = cytoscape({
            container: document.getElementById('reconfirmed'),
            layout: styles,
            style: dataArray[0],
            elements: dataArray[1].response
        });
        cy_reconfirmed.minZoom(2);
        cy_reconfirmed.maxZoom(10);
    });
}

document.getElementById("reset_reconfirmed").addEventListener("click", resetReconfirmed);
function resetReconfirmed() {
    cy_reconfirmed.destroy();
    initReconfirmed();
}
