document.addEventListener("DOMContentLoaded", function (event) {
    let GalleryWrapper = document.querySelector('.gallery-wrapper');
    if (GalleryWrapper) {
        let iso = new Isotope('.gallery-wrapper', {
            itemSelector: '.element-item',
            layoutMode: 'fitRows'
        });
    }
    let lightbox = GLightbox({
        selector: '.image-popup',
        title: false,
    });
})

let labelPercentFormatter = function(value) {
  return value + "%";
};
let optionsCPUUsedArea = {
    series: [],
    chart: {
        id: 'cpu',
        group: 'op_status',
        type: 'area',
        height: 200,
        zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    title: {
        text: 'CPU Used',
        align: 'center',
        style: {
            fontWeight: 500,
        },
    },
    colors: ['#4B38AA'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'straight',
        width: 3,
    },
    toolbar: {
        tools: {
            selection: false
        }
    },
    markers: {
        size: 0
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
        },
    },
    tooltip: {
        followCursor: false,
        x: {
            show: false
        },
        marker: {
            show: false
        },
        y: {
            title: {
                formatter: function () {
                    return ''
                }
            }
        }
    },
    grid: {
        clipMarkers: false
    },
    yaxis: {
        min:0,
        max:100,
        tickAmount: 2,
        title: {text:"Utilization Rate(%)"},
         labels: {
            formatter: labelPercentFormatter
         }
    },
    xaxis: {
        type: 'datetime',
        labels: {
            formatter: function(value, timestamp, opts) {
              return opts.dateFormatter(new Date(timestamp), 'HH:mm:ss')
            }
        },
    }
};
let CPUUsedArea = new ApexCharts(document.querySelector("#cpu-used-area"), optionsCPUUsedArea);
CPUUsedArea.render();

let optionsMemUsedArea = {
    series: [],
    chart: {
        id: 'memory',
        group: 'op_status',
        type: 'area',
        height: 200,
        zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    title: {
        text: 'Memory Used',
        align: 'center',
        style: {
            fontWeight: 500,
        },
    },
    colors: ['#FFBE0B'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    toolbar: {
        tools: {
            selection: false
        }
    },
    markers: {
        size: 0
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
        },
    },
    tooltip: {
        followCursor: false,
        x: {
            show: false
        },
        marker: {
            show: false
        },
        y: {
            title: {
                formatter: function () {
                    return ''
                }
            }
        }
    },
    grid: {
        clipMarkers: false
    },
    yaxis: {
        min:0,
        max:100,
        tickAmount: 2,
        title: {text:"Utilization Rate(%)"},
        labels: {
            formatter: labelPercentFormatter
        }
    },
    xaxis: {
        type: 'datetime',
        labels: {
            formatter: function(value, timestamp, opts) {
              return opts.dateFormatter(new Date(timestamp), 'HH:mm:ss')
            }
        },
    }
};
let MemUsedArea = new ApexCharts(document.querySelector("#memory-used-area"), optionsMemUsedArea);
MemUsedArea.render();

let labelUnitFormatter = function(value) {
    if (value >= 1048576) {
        value = Math.ceil(value / 1048576) + " MB";
    }
    else if(value >= 1024){
        value = Math.ceil(value / 1024) + " KB";
    }
  return value;
};

let optionsDiskIOArea = {
    series: [],
    chart: {
        id: 'disk',
        group: 'op_status',
        type: 'area',
        height: 200,
        zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    title: {
        text: 'Disk Used',
        align: 'center',
        style: {
            fontWeight: 500,
        },
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
        },
    },
    colors: ['#45CB85', '#F06548'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    toolbar: {
        tools: {
            selection: false
        }
    },
    markers: {
        size: 0
    },
    tooltip: {
        followCursor: false,
        x: {
            show: false
        },
        marker: {
            show: false
        },
        y: {
            title: {
                formatter: function () {
                    return ''
                }
            }
        }
    },
    grid: {
        clipMarkers: false
    },
    yaxis: {
        tickAmount: 2,
        title: {text:"Disk IO(K)"},
         labels: {
            formatter: labelUnitFormatter
          }
    },
    xaxis: {
        type: 'datetime'
    }
};
let diskIOArea = new ApexCharts(document.querySelector("#disk-used-area"), optionsDiskIOArea);
diskIOArea.render();

let url = $("#performance-chart").data("urls");

let updateChartData = function () {
    $.getJSON(url, function(response) {
        let cpu_data = [];
        let mem_data = [];
        let disk_write_io_data = [];
        let disk_read_io_data = [];
        for(let each_data of response){
            cpu_data.push({x:each_data['created_time'], y:each_data['cpu_rate']});
            mem_data.push({x:each_data['created_time'], y:each_data['mem_rate']});
            disk_write_io_data.push({x:each_data['created_time'], y:each_data['disk_write_io']});
            disk_read_io_data.push({x:each_data['created_time'], y:each_data['disk_read_io']});
        }
        CPUUsedArea.updateSeries([{data: cpu_data}]);
        MemUsedArea.updateSeries([{data: mem_data}]);
        diskIOArea.updateSeries([
            {
                name: 'Write IO',
                data: disk_write_io_data,
            },
            {
                name: 'Read IO',
                data: disk_read_io_data,
            },
        ]);});
};
updateChartData()

window.setInterval("updateChartData()", 5000)
