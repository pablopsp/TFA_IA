var data;
const select = document.querySelector("select");

fetch("../data/Ibex35Data.json")
    .then(response => response.json())
    .then(json => {
        data = json;
        json.forEach(companie => {
            opt = document.createElement("option");
            opt.text = companie.brand;

            select.appendChild(opt);
        });
        createChart();
    });

const dataForChart = () => {
    arr = [];
    obj = data[document.querySelector("select").selectedIndex].data;
    Object.keys(obj).forEach(function (key) {
        var obje = new Object();
        (obje.fecha = obj[key][0]),
        (obje.valorCierre = obj[key][1].replace(/,/g, '.')),
        (jsonString = JSON.stringify(obje));
        arr.push(obje);
    });
    return arr;
};

var chart;
const createChart = () => {
    var ctx = document.getElementById("chart").getContext("2d");
     chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dataForChart().map(v => {
                return v.fecha;
            }),
            datasets: [{
                label: document.querySelector("select").value,
                fill: false,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#000",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "#5864E6",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
                borderColor: "rgb(75, 192, 192)",
                data: dataForChart().map(v => {
                    return v.valorCierre;
                })
            }]
        },
        options: {}
    });
};

select.addEventListener("change", () => {
    chart.destroy();
    createChart();
});