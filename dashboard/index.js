var data;
const select = document.querySelector("select");

window.addEventListener(
    'scroll',
    () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            moreData();
         }
    },
    false
);

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
    return arr.reverse();
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
        options: {
            animation: false
        }
    });
};

select.addEventListener("change", () => {
    chart.destroy();
    seeChart();
});

const seeChart = () => {
    if (document.querySelector("table") != undefined)
        document.querySelector("table").remove();
    createChart();
};

const seeRawData = () => {
    chart.destroy();

    const cntent_data = document.querySelector(".cntent_data");

    const obj = data[document.querySelector("select").selectedIndex].data;
    const trs = Object.keys(obj.slice(0,24)).map(function (key) {
        return trTemplate(obj[key]);
    }).join("");

    const table =
        `<table>
            <thead>
            <tr>
                <th>Fecha</th>
                <th>Cierre</th>
                <th>Var. (€)</th>
                <th>Var. (%)</th>
                <th>Máx</th>
                <th>Mín</th>
                <th>Volumen (€)</th>
            </tr>
            </thead>
            <tbody class="bordered">
                ${trs}
            </tbody>
        </table>
    `;
    document.querySelector(".chrt_data").style.height = "10px";
    cntent_data.innerHTML = table;
}

const moreData = () => {
    const obj = data[document.querySelector("select").selectedIndex].data;

    const trLength = document.querySelectorAll("tr").length;
    if(trLength != 0){
        const trs = Object.keys(obj.slice(0, trLength+24)).map(function(key) {
            return trTemplate(obj[key]);
        }).join("");
        document.querySelector(".bordered").innerHTML = trs;
    }
};


const trTemplate = (values) => {
    return `
        <tr>
            <td>${values[0]}</td>
            <td>${values[1]}</td>
            <td>${values[2]}</td>
            <td>${values[3]}</td>
            <td>${values[4]}</td>
            <td>${values[5]}</td>
            <td>${values[6]}</td>
        </tr>
    `;
}