let log_statistic_chart_option = {
    chart: {
        height: 345,
        type: 'bar',
        zoom: {
            enabled: false
        },
        toolbar: {
            show: false,
        }
    },
    colors: ['#45CB85', '#4B38B3'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [3, 4, 3],
        curve: 'straight',
    },
    series: [],
    markers: {
        size: 0,
        hover: {
            sizeOffset: 6
        }
    },
    xaxis: {
        type: 'date'
    },
    yaxis: [
      {
        labels: {
          formatter: function(val) {
            return val.toFixed(0);
          }
        }
      }
    ],
    grid: {
        borderColor: '#f1f1f1',
    }
}

let chart = new ApexCharts(
    document.querySelector("#log_statistic_chart"),
    log_statistic_chart_option
);

chart.render();

let get_daily_log = function (user_id) {
    $.ajax({
        type: 'get',
        url: `log-chart-data/${user_id}`,
        data: {},
        success: function (data) {
            let daily_event_log_data = data['events'];
            let daily_operations_log_data = data['operations'];
            chart.updateSeries([
                {name:"Event Log", data: daily_event_log_data},
                {name:"Operation Log", data: daily_operations_log_data},
            ]);
        }
    });
};

get_daily_log(4);
