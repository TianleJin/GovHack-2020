function initMap() {
    // The location of Uluru
    var uluru = {lat: -25.344, lng: 131.036};
    // The map, centered at Uluru
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 4, center: uluru});
    // The marker, positioned at Uluru
    var marker = new google.maps.Marker({position: uluru, map: map});
}

var ctx = document.getElementById("radar-chart").getContext("2d")
var radar_chart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ["Population","Median Age","Median Rent","Median House Price"],
        datasets: [{
            label: "Lynbrook",
            data: [8519,39,410,622]
        }]
    },
    options:Chart.defaults.radar
});

function updateChart(area,pop,age,rent,own) {
    radar_chart.data.datasets = [{
        label: area,
        data: [pop,age,rent,own]
    }]
    radar_chart.update()
}

function yeet() {
    if (radar_chart.data.datasets[0].label == "Lynbrook") {
        updateChart("South Yarra",25147,33,750,1690)
    } else {
        updateChart("Lynbrook",8519,39,410,622)
    }
}