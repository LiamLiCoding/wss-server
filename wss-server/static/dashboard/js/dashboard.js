let get_event_log = function (device_id) {
    $.ajax({
        type: 'get',
        url: `record/event-log-by-user/${device_id}`,
        data: {},
        success: function (data) {
            console.log(data)
        }
    });
}

let log_statistic_chart_option = {
    chart: {
        height: 345,
        type: 'line',
        zoom: {
            enabled: false
        },
        toolbar: {
            show: false,
        }
    },
    colors: ['#45CB85', '#4B38B3', '#3577F1'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [3, 4, 3],
        curve: 'straight',
        dashArray: [0, 8, 5]
    },
    series: [{
        name: 'New Application',
        data: [89, 56, 74, 98, 72, 38, 64, 46, 84, 58, 46, 49]
    },
    {
        name: "Interview",
        data: [45, 52, 38, 24, 33, 26, 21, 20, 6, 8, 15, 10]
    },
    {
        name: " Hired",
        data: [36, 42, 60, 42, 13, 18, 29, 37, 36, 51, 32, 35]
    }
    ],
    markers: {
        size: 0,

        hover: {
            sizeOffset: 6
        }
    },
    xaxis: {
        categories: ['01 Jan', '02 Jan', '03 Jan', '04 Jan', '05 Jan', '06 Jan', '07 Jan', '08 Jan', '09 Jan',
            '10 Jan', '11 Jan', '12 Jan'
        ],
    },
    grid: {
        borderColor: '#f1f1f1',
    }
}

let chart = new ApexCharts(
    document.querySelector("#log_statistic_chart"),
    log_statistic_chart_option
);

chart.render();

